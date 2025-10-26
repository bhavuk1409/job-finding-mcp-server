# Jobs and Internships MCP Server

A Model Context Protocol (MCP) server providing comprehensive job and internship search capabilities using the Adzuna Jobs API.

## Features

- **Universal job search** - All industries and job types
- **Internship search** - Dedicated internship finder
- **Company-specific search** - Jobs at specific companies (enhanced filtering)
- **Remote opportunities** - Filter for remote positions
- **Category browsing** - Industry-wise job categories
- **Global coverage** - Search by country/location

## Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd ai-internships-mcp-server

# Install dependencies
pip install fastmcp httpx python-dotenv

# Setup environment
cp .env.example .env
# Add your Adzuna credentials to .env

# Run the server
uv run fastmcp dev app.py
```

## API Integration

- **Adzuna Jobs API** - Primary job aggregation platform
  - Global coverage with country-specific searches
  - Rich metadata (salary, contract type, categories)
  - No RapidAPI dependency required

## Setup Instructions

1. **Adzuna API Setup**:
   - Sign up at [Adzuna Developer](https://developer.adzuna.com/)
   - Create an application to get App ID and App Key
   - Add to `.env`:
     ```
     ADZUNA_APP_ID=your_app_id
     ADZUNA_APP_KEY=your_app_key
     ```

## Available Tools

1. **search_jobs** - Universal job search across all industries
2. **search_internships** - Dedicated internship opportunities
3. **search_company_jobs** - Jobs at specific companies (enhanced filtering)
4. **get_job_categories** - Browse job categories by industry
5. **search_remote_jobs** - Remote work opportunities

## Usage Examples

```bash
# Start the server
uv run fastmcp dev app.py

# Example searches:
search_jobs("Software Engineer", "Bangalore", "in", 1, 20)
search_company_jobs("Google", "", "India", "in", 1, 20)
search_remote_jobs("Python Developer", "in", 1, 20)
```

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

## Recent Improvements

- **Fixed company search**: Enhanced filtering for accurate company-specific results
- **Better matching**: Improved company name matching logic
- **Cleaner code**: Removed debug elements, added professional documentation
- **GitHub ready**: Clean codebase with proper error handling

## Project Structure
```
ai-internships-mcp-server/
├── app.py              # Main MCP server
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Your API credentials (gitignored)
├── .gitignore         # Git ignore rules
└── README.md          # This documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.
