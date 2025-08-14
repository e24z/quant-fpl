BUDGET=100.0
QUOTAS = {"GK":2, "DEF":5, "MID":5, "FWD":3}
team_cap = 3

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

    
