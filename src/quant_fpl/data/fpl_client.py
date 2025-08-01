from pydantic import BaseModel, ConfigDict

class FplClient(BaseModel):
    model_config = ConfigDict(frozen = True)

    base_url: str = "https://fantasy.premierleague.com/api"
            
