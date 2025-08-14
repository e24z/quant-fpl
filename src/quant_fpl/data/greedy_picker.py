import pandas as pd

BUDGET=100.0
QUOTAS = {"GK":2, "DEF":5, "MID":5, "FWD":3}
team_cap = 3

VALID_XI = [(3,4,3),(3,5,2),(4,4,2),(4,3,3),(4,5,1),(5,3,2),(5,2,3),(5,4,1)]

def assert_squad_constraints(squad): # TODO: a pydantic model might be better suited here.
    """Recieve a dataframe of players and assert that:
        - squad size <= 15
        - squad cost <= 100m
        - positional quotas met
        - club cap <= 3"""

    assert len(squad) == 15, 'need 15 players'
    assert float(squad["price"].sum()) <= BUDGET + 1e-9, "over budget"
    
    # use dict as source of truth
    for pos, quota in QUOTAS.items():
        assert (squad["pos"]==pos).sum() == quota, f"{pos} wrong count"

    per_club = squad.groupby("team")["id"].count()
    assert (per_club <= 3).all(), "club cap > 3"

def greedy_squad(df):
    picked = []
    spend = 0.0
    team_counts = {t: 0 for t in df["team"].unique()}

    for pos, quota in QUOTAS.items():
        pool = df[df["pos"] == pos].sort_values(["value", "ppg"], ascending=False)
        taken = 0
        for _, row in pool.iterrows():
            team_id = row["team"]
            price = float(row["price"])
            if team_counts[team_id] >= 3:
                continue
            if spend + price > BUDGET + 1e-9:
                continue
            picked.append(row.to_dict())
            spend += price
            team_counts[team_id] += 1
            taken += 1
            if taken == quota:
                break

    squad = pd.DataFrame(picked)
    assert_squad_constraints(squad)
    return squad

def pick_xi(squad):
    def top(df, pos, n):
        return df[df["pos"]==pos].sort_values(["value","ppg"], ascending=False).head(n)

    gk1 = top(squad, "GK", 1)
    for d, m, f in VALID_XI:
        xi = pd.concat([gk1, top(squad,"DEF",d), top(squad,"MID",m), top(squad,"FWD",f)], ignore_index=True)
        if len(xi) != 11:
            continue
        # bench = the other 4 (GK first, then outfield by ascending value)
        leftovers = squad.merge(xi[["id"]], on="id", how="left", indicator=True)
        bench = leftovers[leftovers["_merge"]=="left_only"].drop(columns=["_merge"])
        bench = pd.concat([bench[bench.pos=="GK"],
                           bench[bench.pos!="GK"].sort_values(["value","ppg"])],
                          ignore_index=True)
        # C / VC = top ppg in XI
        xi_sorted = xi.sort_values(["ppg","value"], ascending=False)
        C_id, VC_id = int(xi_sorted.iloc[0]["id"]), int(xi_sorted.iloc[1]["id"])
        return xi, f"{d}-{m}-{f}", bench, (C_id, VC_id)
    raise RuntimeError("Could not form a valid XI")

    
