from pydantic import BaseModel, ConfigDict, Field
import httpx
import pandas as pd
from datetime import datetime

class Player(BaseModel):
    """Subset of fields we care about."""
    id: int
    web_name: str
    now_cost: int = Field(ge=0) # TODO: Check typing... 

class FPLClient(BaseModel):
    """Wrapper around the FPL API."""
    BASE_URL: str = "https://fantasy.premierleague.com/api"
    timeout_s: int = 15

    model_config = ConfigDict(frozen = True)

    async def _get_json(self, path: str) -> dict:
        """Takes an endpoint, sends a GET request and returns JSON object."""

        url = f"{self.BASE_URL}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=self.timeout_s) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    
            
    async def bootstrap(self) -> pd.DataFrame:
        """Fetch the bootstrap-static payload and return the `elements` table."""

        payload = await self._get_json("bootstrap-static/")
        raw_players: list[dict] = payload["elements"]

        Player.model_validate(raw_players[0])

        df = pd.DataFrame(raw_players)
        df["snapshot_ts"] = datetime.utcnow()
        return df

if __name__ == "__main__":
    import asyncio

    async def main():
        from quant_fpl.data.fpl_client import FPLClient

        client = FPLClient()
        data = await client.bootstrap()
        print(f"Fetched {len(data)} players.")

    asyncio.run(main())