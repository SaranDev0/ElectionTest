def predict_pm(elections, predictions):
    seat_winners = {}

    for p in predictions:
        cid = p["constituency_id"]
        if cid not in seat_winners or p["win_probability"] > seat_winners[cid]["win_probability"]:
            seat_winners[cid] = p

    party_seats = {}

    for winner in seat_winners.values():
        party = elections.loc[
            elections["candidate_id"] == winner["candidate_id"],
            "party"
        ].values[0]

        party_seats[party] = party_seats.get(party, 0) + 1

    if not party_seats:
        return {"pm_party": "N/A", "seats": 0, "majority": False}

    pm_party = max(party_seats, key=party_seats.get)
    seats = party_seats[pm_party]
    total_seats = len(seat_winners)
    majority = seats >= (total_seats // 2 + 1)

    return {
        "pm_party": pm_party,
        "seats": seats,
        "majority": majority
    }
