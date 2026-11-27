# Story ID: SCHEDULING-BE-001.1
# Scenario ID: SCHEDULING-BE-001.1-S1

from src.present_management import presents
from src.scheduling import assign_present_to_elf, available_elves, busy_elves


def test_scheduling_be_001_1_s1_assign_available_present():
    # GIVEN: The available_elves set contains elf "E001"
    available_elves.clear()
    available_elves.add("E001")

    # AND: The busy_elves dictionary is empty
    busy_elves.clear()

    # AND: Present "P001" is available from Present Management
    presents.clear()
    presents["P001"] = {
        "present_id": "P001",
        "family_id": "F001",
        "status": "available",
    }

    # WHEN: assign_present_to_elf is called
    assignment = assign_present_to_elf(present_id="P001", elf_id="E001")

    # THEN: Elf "E001" is removed from available_elves
    assert "E001" not in available_elves

    # AND: Elf "E001" is added to busy_elves with value "P001"
    assert busy_elves["E001"] == "P001"

    # AND: The assignment record is returned
    assert assignment is not None

    # AND: Present status is updated to "assigned"
    assert presents["P001"]["status"] == "assigned"
