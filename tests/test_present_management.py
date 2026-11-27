# Story ID: PRESENT-BE-001.1
# Scenario ID: PRESENT-BE-001.1-S1

import threading

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


# Story ID: PRESENT-BE-001.2
# Scenario ID: PRESENT-BE-001.2-S1


def test_present_be_001_2_s1_given_concurrent_arrivals_then_both_stored():
    # GIVEN: An empty present inventory
    presents.clear()
    family_groups.clear()

    # Track exceptions raised in worker threads
    exceptions = []

    # Worker function for both threads
    def toy_machine_worker(present_id, family_id):
        try:
            barrier.wait(timeout=5.0)
            receive_present(present_id=present_id, family_id=family_id)
        except Exception as e:
            exceptions.append(e)

    # Use barrier to synchronize both threads before calling receive_present
    barrier = threading.Barrier(2)

    # Create and start threads
    thread_a = threading.Thread(
        target=toy_machine_worker, args=("P001", "F001"), name="ToyMachine-A"
    )
    thread_b = threading.Thread(
        target=toy_machine_worker, args=("P002", "F002"), name="ToyMachine-B"
    )

    thread_a.start()
    thread_b.start()

    # Assert both threads completed successfully
    thread_a.join(timeout=5.0)
    thread_b.join(timeout=5.0)

    assert not thread_a.is_alive(), "ToyMachine-A thread did not complete"
    assert not thread_b.is_alive(), "ToyMachine-B thread did not complete"

    # Assert no exceptions occurred in worker threads
    assert len(exceptions) == 0, f"Exceptions raised in worker threads: {exceptions}"

    # THEN: Both presents are added to the inventory without conflict
    assert presents["P001"] == {
        "present_id": "P001",
        "family_id": "F001",
        "status": "available",
    }
    assert presents["P002"] == {
        "present_id": "P002",
        "family_id": "F002",
        "status": "available",
    }

    # AND: No duplicate entries or lost updates occur
    assert len(presents) == 2

    # AND: Each family group contains the correct present
    assert len(family_groups) == 2
    assert "F001" in family_groups
    assert "F002" in family_groups
    assert "P001" in family_groups["F001"]
    assert "P002" in family_groups["F002"]
