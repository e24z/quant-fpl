from pydantic import BaseModel, ConfigDict
import httpx
import pandas as pd

class FplClient(BaseModel):
    """Wrapper around the FPL API."""
    BASE_URL: str = "https://fantasy.premierleague.com/api"
    timeout_s: int = 15

    model_config = ConfigDict(frozen = True)

    async def _get_json(self, path: str) -> dict:
        """Takes an endpoint, sends a GET request and returns JSON object."""

        url = f"{self.BASE_URL}/{path.lstrip("/")}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    
            
    async def bootstrap(self) -> pd.DataFrame:
        """Fetch the bootstrap-static payload and return the `elements` table."""
