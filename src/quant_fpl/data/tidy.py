import pandas as pd

POS_MAP = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}

def tidy_payload(payload: dict) -> pd.DataFrame:
    players = pd.DataFrame(payload["elements"]).copy()
    teams = pd.DataFrame(payload["teams"])[["id","name"]].rename(columns={"id":"team_id","name":"club"})
    types = pd.DataFrame(payload["element_types"])[["id"]].rename(columns={"id":"type_id"})

    players["price"] = players["now_cost"].astype(float) / 10.0
    players["ppg"] = pd.to_numeric(players["points_per_game"], errors="coerce").fillna(0.0)
    players["pos"] = players["element_type"].map(POS_MAP)
    out = players.merge(teams, left_on="team", right_on="team_id", how="left")
    out = out[out["status"] == "a"]  # basic availability
    return out[["id","web_name","pos","club","team","price","ppg"]].reset_index(drop=True)
    
