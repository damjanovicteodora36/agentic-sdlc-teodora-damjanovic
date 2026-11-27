"""Present Management component."""

presents = {}
family_groups = {}


def receive_present(present_id: str, family_id: str) -> None:
    """Store a present and associate it with its family."""

    presents[present_id] = {
        "present_id": present_id,
        "family_id": family_id,
        "status": "available",
    }

    if family_id not in family_groups:
        family_groups[family_id] = []

    family_groups[family_id].append(present_id)
