# Story ID: PRESENT-BE-001.1
# Scenario ID: PRESENT-BE-001.1-S1

from src.present_management import (
    family_groups,
    presents,
    receive_present,
)


def test_receive_present_stores_new_present():
    # GIVEN: An empty present inventory
    presents.clear()
    family_groups.clear()

    # WHEN: A new present is received
    receive_present(present_id="P001", family_id="F001")

    # THEN: The present is stored with the correct fields
    assert presents["P001"] == {
        "present_id": "P001",
        "family_id": "F001",
        "status": "available",
    }

    # AND: The present belongs to the correct family group
    assert family_groups["F001"] == ["P001"]
