# Jobs & Internships MCP Server

A **Model Context Protocol (MCP) server** for searching jobs and internships
through the **Adzuna Jobs API** — universal job search, dedicated internship
search, company-specific filtering, and remote-only results, all callable as
MCP tools from any compatible client.

![python](https://img.shields.io/badge/python-3.x-3776ab) ![framework](https://img.shields.io/badge/framework-FastMCP-6e56cf) ![api](https://img.shields.io/badge/data-Adzuna%20Jobs%20API-ff6f00) ![license](https://img.shields.io/badge/license-MIT-green)

---

## What it does

- **Universal job search** — query across all industries and job types.
- **Internship search** — a dedicated finder for internship listings.
- **Company-specific search** — enhanced filtering for jobs at a named
  company, with improved company-name matching.
- **Remote opportunities** — filter results down to remote-only positions.
- **Category browsing** — list job categories by industry.
- **No RapidAPI dependency** — talks directly to Adzuna, with global,
  country-specific coverage and rich metadata (salary, contract type,
  category).

---

## Repository layout

```
├── app.py               # Main MCP server (tools + Adzuna integration)
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
├── uv.lock              # Dependency lock file
├── .env.example         # Environment variable template
├── .env                 # Your API credentials (gitignored)
└── README.md            # This file
```

---

## Quickstart

### 1. Get Adzuna API credentials

- Sign up at [Adzuna Developer](https://developer.adzuna.com/)
- Create an application to get an **App ID** and **App Key**

### 2. Install & configure

```bash
git clone https://github.com/bhavuk1409/job-finding-mcp-server.git
cd job-finding-mcp-server

pip install fastmcp httpx python-dotenv

cp .env.example .env
```

Add your credentials to `.env`:

```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

### 3. Run

```bash
uv run fastmcp dev app.py
```

---

## Tools

| Name | Description |
| --- | --- |
| `search_jobs` | Universal job search across all industries |
| `search_internships` | Dedicated internship search |
| `search_company_jobs` | Jobs at a specific company, with enhanced filtering |
| `get_job_categories` | Browse job categories by industry |
| `search_remote_jobs` | Remote-only job opportunities |

**Example calls:**

```python
search_jobs("Software Engineer", "Bangalore", "in", 1, 20)
search_company_jobs("Google", "", "India", "in", 1, 20)
search_remote_jobs("Python Developer", "in", 1, 20)
```

---

## Integration with Claude Desktop

```json
{
  "mcpServers": {
    "jobs-platform": {
      "command": "python3",
      "args": ["actual_path"],
      "cwd": "/path/to/mcp-server"
    }
  }
}
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes (add tests if applicable)
4. Submit a pull request

---

## Support

For issues and questions, please open a GitHub issue.

---

## License

MIT
