#!/usr/bin/env python3
"""
Jobs and Internships MCP Server

A Model Context Protocol server that aggregates job and internship listings 
from Adzuna job platform for comprehensive career opportunities.

Author: Bhavuk Agrawal
License: MIT
"""

import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict

import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("jobs-internships-server")


class JobsFetcher:
    """
    Main class for fetching job and internship data from Adzuna platform.
    
    Provides comprehensive job listings across all industries and experience levels.
    """
    
    def __init__(self):
        """Initialize the fetcher with Adzuna API configuration."""
        self.client = httpx.AsyncClient(timeout=30.0)
        
        # Adzuna API configuration
        self.adzuna_app_id = os.getenv("ADZUNA_APP_ID")
        self.adzuna_app_key = os.getenv("ADZUNA_APP_KEY")
        self.adzuna_base_url = "https://api.adzuna.com/v1/api/jobs"
    
    async def search_jobs(
        self,
        what: str = "",
        where: str = "India",
        country: str = "in",
        page: int = 1,
        results_per_page: int = 20
    ) -> List[Dict]:
        """
        Search Adzuna for job listings.
        
        Args:
            what: Job search keywords (e.g., "Software Engineer", "Marketing Intern")
            where: Location to search (e.g., "India", "Bangalore", "Mumbai")
            country: Country code ("in" for India, "us" for USA, "uk" for UK)
            page: Page number for pagination
            results_per_page: Number of results per page (max: 50)
            
        Returns:
            List of standardized job dictionaries
        """
        try:
            url = f"{self.adzuna_base_url}/{country}/search/{page}"
            params = {
                "app_id": self.adzuna_app_id,
                "app_key": self.adzuna_app_key,
                "results_per_page": results_per_page,
                "what": what,
                "where": where
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_job_results(data)
        except Exception:
            return []
    
    async def search_internships(
        self,
        field: str = "",
        where: str = "India",
        country: str = "in",
        page: int = 1,
        results_per_page: int = 20
    ) -> List[Dict]:
        """
        Search specifically for internship opportunities.
        
        Args:
            field: Field or industry (e.g., "Software", "Marketing", "Finance")
            where: Location to search
            country: Country code
            page: Page number for pagination
            results_per_page: Number of results per page
            
        Returns:
            List of internship opportunities
        """
        search_terms = f"{field} Intern" if field else "Intern"
        return await self.search_jobs(search_terms, where, country, page, results_per_page)
    
    async def search_by_company(
        self,
        company_name: str,
        where: str = "India",
        country: str = "in",
        page: int = 1,
        results_per_page: int = 20
    ) -> List[Dict]:
        """
        Search for jobs at a specific company.
        
        Args:
            company_name: Name of the company
            where: Location to search
            country: Country code
            page: Page number for pagination
            results_per_page: Number of results per page
            
        Returns:
            List of jobs at the specified company
        """
        # Search with company name and filter results by company name match
        all_jobs = await self.search_jobs(company_name, where, country, page, results_per_page * 3)  # Get more results to filter
        
        # Filter jobs where the company name matches (case-insensitive)
        company_lower = company_name.lower().strip()
        filtered_jobs = []
        
        for job in all_jobs:
            job_company = job.get("company", "").lower().strip()
            # Check if company name matches exactly or is contained in the job company name
            if (company_lower == job_company or 
                company_lower in job_company or 
                job_company in company_lower):
                filtered_jobs.append(job)
                if len(filtered_jobs) >= results_per_page:
                    break
        
        return filtered_jobs
    
    async def get_job_categories(
        self,
        country: str = "in"
    ) -> List[Dict]:
        """
        Get available job categories from Adzuna.
        
        Args:
            country: Country code
            
        Returns:
            List of job categories
        """
        try:
            url = f"{self.adzuna_base_url}/{country}/categories"
            params = {
                "app_id": self.adzuna_app_id,
                "app_key": self.adzuna_app_key
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data.get("results", [])
        except Exception:
            return []
    
    def _parse_job_results(self, data: Dict) -> List[Dict]:
        """
        Parse Adzuna API response into standardized format.
        
        Args:
            data: Raw Adzuna API response
            
        Returns:
            List of standardized job dictionaries
        """
        jobs = []
        results = data.get("results", [])
        
        for job in results:
            company = job.get("company", {})
            if isinstance(company, dict):
                company_name = company.get("display_name", "Unknown Company")
            else:
                company_name = str(company) if company else "Unknown Company"
            
            location = job.get("location", {})
            if isinstance(location, dict):
                location_str = location.get("display_name", "")
                area = location.get("area", [])
                if area and len(area) > 1:
                    location_str = f"{area[-1]}, {area[-2]}" if len(area) >= 2 else area[0]
            else:
                location_str = str(location) if location else ""
            
            category = job.get("category", {})
            category_name = category.get("label", "") if isinstance(category, dict) else ""
            
            # Determine if it's an internship
            title = job.get("title", "").lower()
            is_internship = any(keyword in title for keyword in ["intern", "trainee", "apprentice"])
            
            # Determine if it's remote
            is_remote = "remote" in location_str.lower() if location_str else False
            
            job_info = {
                "title": job.get("title", ""),
                "company": company_name,
                "location": location_str,
                "description": job.get("description", ""),
                "posted_date": job.get("created", ""),
                "job_id": job.get("id", ""),
                "apply_url": job.get("redirect_url", ""),
                "salary": self._format_salary(job.get("salary_min"), job.get("salary_max")),
                "contract_type": job.get("contract_type", ""),
                "contract_time": job.get("contract_time", ""),
                "remote": is_remote,
                "category": category_name,
                "is_internship": is_internship,
                "source": "Adzuna"
            }
            
            jobs.append(job_info)
        
        return jobs
    
    def _format_salary(self, min_salary, max_salary) -> str:
        """Format salary information."""
        if min_salary and max_salary:
            return f"₹{min_salary:,} - ₹{max_salary:,}"
        elif min_salary:
            return f"₹{min_salary:,}+"
        elif max_salary:
            return f"Up to ₹{max_salary:,}"
        else:
            return "Not specified"
    
    async def close(self):
        """Close the HTTP client connection."""
        await self.client.aclose()


# === MCP TOOLS ===

# Global fetcher instance
fetcher = JobsFetcher()


@mcp.tool()
async def search_jobs(
    keywords: str = "",
    location: str = "India",
    country: str = "in",
    page: int = 1,
    results_per_page: int = 20
) -> str:
    """
    Search for job opportunities across all industries.
    
    Args:
        keywords: Job search keywords (e.g., "Software Engineer", "Marketing Manager")
        location: Location to search (e.g., "India", "Bangalore", "Mumbai")
        country: Country code ("in" for India, "us" for USA, "uk" for UK)
        page: Page number for pagination (default: 1)
        results_per_page: Number of results per page (default: 20, max: 50)
        
    Returns:
        JSON string with job listings
    """
    results = await fetcher.search_jobs(keywords, location, country, page, results_per_page)
    
    return json.dumps({
        "search_terms": keywords,
        "location": location,
        "country": country,
        "page": page,
        "jobs": results,
        "total_found": len(results),
        "timestamp": datetime.now().isoformat()
    }, indent=2)



@mcp.tool()
async def search_company_jobs(
    company_name: str,
    job_description: str = "",
    location: str = "India",
    country: str = "in",
    page: int = 1,
    results_per_page: int = 20
) -> str:
    """
    Search for job opportunities at a specific company.
    
    Args:
        company_name: Name of the company to search
        job_description: Job description or title to filter
        location: Location to search
        country: Country code
        page: Page number for pagination
        results_per_page: Number of results per page
        
    Returns:
        JSON string with company job listings
    """
    results = await fetcher.search_by_company(company_name, location, country, page, results_per_page)
    
    return json.dumps({
        "company": company_name,
        "job_description": job_description,
        "location": location,
        "country": country,
        "page": page,
        "jobs": results,
        "total_found": len(results),
        "timestamp": datetime.now().isoformat()
    }, indent=2)


@mcp.tool()
async def search_remote_jobs(
    keywords: str = "",
    country: str = "in",
    page: int = 1,
    results_per_page: int = 20
) -> str:
    """
    Search specifically for remote job opportunities.
    
    Args:
        keywords: Job search keywords
        country: Country code to search within
        page: Page number for pagination
        results_per_page: Number of results per page
        
    Returns:
        JSON string with remote job listings
    """
    search_terms = f"{keywords} remote" if keywords else "remote"
    results = await fetcher.search_jobs(search_terms, "Remote", country, page, results_per_page)
    
    # Filter to ensure we only return remote jobs
    remote_jobs = [job for job in results if job.get("remote", False)]
    
    return json.dumps({
        "search_terms": keywords,
        "country": country,
        "page": page,
        "remote_jobs": remote_jobs,
        "total_found": len(remote_jobs),
        "timestamp": datetime.now().isoformat()
    }, indent=2)


def main():
    """Run the FastMCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
