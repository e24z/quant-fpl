import pandas as pd

POS_MAP = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}

def tidy_payload(payload: dict) -> pd.DataFrame:
    df = pd.DataFrame(payload["elements"]).copy()
    teams = pd.DataFrame(payload["teams"])[["id", "name"]].rename(
        columns={"id": "team_id", "name": "club"}
    )

    df["price"] = df["now_cost"].astype(float) / 10.0
    df["ppg"] = pd.to_numeric(df["points_per_game"], errors="coerce").fillna(0.0)
    df["pos"] = df["element_type"].map(POS_MAP)
    df["selected_by_percent"] = pd.to_numeric(df["selected_by_percent"], errors="coerce").fillna(0.0)

    df = df.merge(teams, left_on="team", right_on="team_id", how="left")
    df = df[df["status"] == "a"]
    df = df[(df["minutes"] >= 900) | (df["selected_by_percent"] >= 5)]
    df["value"] = df["ppg"] / df["price"].replace(0, pd.NA)

    return df[["id", "web_name", "pos", "club", "team", "price", "ppg", "value"]].reset_index(drop=True)    
