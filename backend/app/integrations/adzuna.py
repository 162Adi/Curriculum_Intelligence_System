"""
Adzuna Job Market Provider Adapter with verified India tech snapshot fallback.
Retrieves and parses job listings across Bengaluru, Hyderabad, Pune, Mumbai, and NCR.
"""

import httpx
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.core.config import settings


class AdzunaClient:
    """Official Adzuna API client for Indian technology markets."""

    BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    def __init__(self, app_id: Optional[str] = None, app_key: Optional[str] = None):
        self.app_id = app_id or settings.ADZUNA_APP_ID
        self.app_key = app_key or settings.ADZUNA_APP_KEY

    def is_configured(self) -> bool:
        """Check if official credentials are provided."""
        return bool(self.app_id and self.app_key)

    async def fetch_jobs(self, query: str = "Software Engineer", location: str = "Bengaluru", limit: int = 20) -> Dict[str, Any]:
        """Fetch live listings from Adzuna if configured, else return structured integration note."""
        if not self.is_configured():
            return {
                "status": "NOT_CONFIGURED",
                "is_live": False,
                "message": "Adzuna credentials (ADZUNA_APP_ID / ADZUNA_APP_KEY) not configured. Using verified curated market snapshot.",
                "jobs": [],
                "retrieved_at": datetime.now(timezone.utc).isoformat()
            }

        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": min(limit, 50),
            "what": query,
            "where": location,
            "content-type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(self.BASE_URL, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    jobs = []
                    for item in data.get("results", []):
                        jobs.append({
                            "job_id": str(item.get("id")),
                            "title": item.get("title", "Software Engineer"),
                            "company": item.get("company", {}).get("display_name", "Technology Enterprise"),
                            "location": item.get("location", {}).get("display_name", location),
                            "salary_min": item.get("salary_min"),
                            "salary_max": item.get("salary_max"),
                            "description": item.get("description", ""),
                            "url": item.get("redirect_url"),
                            "source_date": item.get("created")
                        })
                    return {
                        "status": "SUCCESS",
                        "is_live": True,
                        "data_source": "Adzuna API (Live)",
                        "location": location,
                        "total_count": data.get("count", len(jobs)),
                        "jobs": jobs,
                        "retrieved_at": datetime.now(timezone.utc).isoformat()
                    }
                else:
                    return {
                        "status": "API_ERROR",
                        "is_live": False,
                        "message": f"Adzuna API returned status code {resp.status_code}: {resp.text[:200]}",
                        "jobs": [],
                        "retrieved_at": datetime.now(timezone.utc).isoformat()
                    }
        except Exception as e:
            return {
                "status": "CONNECTION_FAILED",
                "is_live": False,
                "message": f"Failed to connect to Adzuna endpoint: {str(e)}",
                "jobs": [],
                "retrieved_at": datetime.now(timezone.utc).isoformat()
            }
