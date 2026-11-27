# Story ID: SCHEDULING-BE-001.1
# Scenario ID: SCHEDULING-BE-001.1-S1

import threading

from src.present_management import (
    family_groups,
    get_available_presents,
    presents,
    receive_present,
)
from src.scheduling import (
    assign_present_to_elf,
    available_elves,
    busy_elves,
    elf_assignment_completed,
)


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


# Story ID: SCHEDULING-BE-001.2
# Scenario ID: SCHEDULING-BE-001.2-S1


def test_scheduling_be_001_2_s1_atomic_elf_assignment():
    # GIVEN: The available_elves set contains elf "E001" only
    available_elves.clear()
    available_elves.add("E001")

    # AND: The busy_elves dictionary is empty
    busy_elves.clear()

    # AND: Present "P001" and "P002" are available from Present Management
    presents.clear()
    presents["P001"] = {
        "present_id": "P001",
        "family_id": "F001",
        "status": "available",
    }
    presents["P002"] = {
        "present_id": "P002",
        "family_id": "F002",
        "status": "available",
    }

    # Track exceptions raised in worker threads
    exceptions = []

    # Track successful assignments
    assignments = []
    assignments_lock = threading.Lock()

    # Worker function: both threads try to assign E001
    def assignment_worker(present_id, elf_id):
        try:
            barrier.wait(timeout=5.0)
            result = assign_present_to_elf(present_id=present_id, elf_id=elf_id)
            with assignments_lock:
                assignments.append(result)
        except Exception as e:
            exceptions.append(e)

    # Use barrier to synchronize both threads
    barrier = threading.Barrier(2)

    # Create threads that BOTH request the same elf E001
    thread_a = threading.Thread(
        target=assignment_worker, args=("P001", "E001"), name="Thread-A"
    )
    thread_b = threading.Thread(
        target=assignment_worker, args=("P002", "E001"), name="Thread-B"
    )

    thread_a.start()
    thread_b.start()

    thread_a.join(timeout=5.0)
    thread_b.join(timeout=5.0)

    # AND: Both threads completed without exceptions
    assert not thread_a.is_alive(), "Thread-A did not complete"
    assert not thread_b.is_alive(), "Thread-B did not complete"
    assert len(exceptions) == 0, f"Unexpected exceptions: {exceptions}"

    # AND: Only one assignment succeeded (atomic availability check)
    successful_assignments = [a for a in assignments if a is not None]
    assert len(successful_assignments) == 1, (
        f"Expected 1 successful assignment, got {len(successful_assignments)}: "
        f"{assignments}"
    )

    # AND: The single successful assignment matches busy_elves["E001"]
    assert successful_assignments[0] == {
        "elf_id": "E001",
        "present_id": busy_elves["E001"],
    }

    # AND: E001 is in busy_elves with exactly one mapping
    assert len(busy_elves) == 1
    assert "E001" in busy_elves

    # AND: E001 is no longer in available_elves
    assert "E001" not in available_elves

    # AND: The assigned present has status "assigned"
    assigned_present = busy_elves["E001"]
    assert presents[assigned_present]["status"] == "assigned"

    # AND: The other present remains "available"
    for pid in ["P001", "P002"]:
        if pid != assigned_present:
            assert presents[pid]["status"] == "available"

    # AND: Present state is consistent
    assert len(successful_assignments) == 1
    assert successful_assignments[0]["elf_id"] == "E001"
    assert successful_assignments[0]["present_id"] == assigned_present


# Story ID: SCHEDULING-INFRA-001.2
# Scenario ID: SCHEDULING-INFRA-001.2-S1


def test_scheduling_infra_001_2_s1_query_available_presents():
    # GIVEN: Present Management maintains presents dictionary with available
    # and assigned presents
    from src.present_management import presents

    presents.clear()

    # AND: Present "P001" is available
    presents["P001"] = {
        "present_id": "P001",
        "family_id": "F001",
        "status": "available",
    }

    # AND: Present "P002" is assigned
    presents["P002"] = {
        "present_id": "P002",
        "family_id": "F002",
        "status": "assigned",
    }

    # AND: Present "P003" is available
    presents["P003"] = {
        "present_id": "P003",
        "family_id": "F003",
        "status": "available",
    }

    # WHEN: get_available_presents() is called on Present Management
    available = get_available_presents()

    # THEN: Only presents with status "available" are returned
    assert len(available) == 2
    assert "P001" in available
    assert "P003" in available

    # AND: Assigned presents are excluded from the result
    assert "P002" not in available

    # AND: The original inventory remains unchanged
    assert len(presents) == 3
    assert presents["P001"]["status"] == "available"
    assert presents["P002"]["status"] == "assigned"
    assert presents["P003"]["status"] == "available"


# Story ID: SCHEDULING-INFRA-001.3
# Scenario ID: SCHEDULING-INFRA-001.3-S1


def test_scheduling_infra_001_3_s1_elf_completion():
    # GIVEN: Elf "E001" has completed loading present "P001" onto the sleigh
    available_elves.clear()
    busy_elves.clear()

    # AND: Present "P001" is assigned to elf "E001"
    presents.clear()
    presents["P001"] = {
        "present_id": "P001",
        "family_id": "F001",
        "status": "assigned",
    }
    busy_elves["E001"] = "P001"

    # AND: Elf "E001" is NOT in available_elves
    assert "E001" not in available_elves

    # WHEN: Sleigh Management calls elf_assignment_completed(elf_id="E001")
    elf_assignment_completed(elf_id="E001")

    # THEN: Elf "E001" is removed from busy_elves
    assert "E001" not in busy_elves

    # AND: Elf "E001" is added to available_elves
    assert "E001" in available_elves


# Story ID: SCHEDULING-STORY-001
# Scenario ID: SCHEDULING-STORY-001-S2


def test_scheduling_story_001_s2_multiple_elf_assignments():
    # GIVEN: Present "P001" and "P002" are in the "available" status
    # in Present Management inventory
    presents.clear()
    presents["P001"] = {
        "present_id": "P001",
        "family_id": "F001",
        "status": "available",
    }
    presents["P002"] = {
        "present_id": "P002",
        "family_id": "F002",
        "status": "available",
    }

    # AND: Elf "E001" and "E002" are in the `available_elves` set
    available_elves.clear()
    available_elves.update(["E001", "E002"])

    # AND: The `busy_elves` dictionary is empty
    busy_elves.clear()

    # WHEN: Mrs Claus calls assign_present_to_elf for both elves
    assignment_1 = assign_present_to_elf(present_id="P001", elf_id="E001")
    assignment_2 = assign_present_to_elf(present_id="P002", elf_id="E002")

    # THEN: Elf "E001" receives present "P001" and is moved to busy_elves
    assert assignment_1 is not None
    assert assignment_1 == {"elf_id": "E001", "present_id": "P001"}
    assert busy_elves["E001"] == "P001"

    # AND: Elf "E002" receives present "P002" and is moved to busy_elves
    assert assignment_2 is not None
    assert assignment_2 == {"elf_id": "E002", "present_id": "P002"}
    assert busy_elves["E002"] == "P002"

    # AND: Both presents are marked as "assigned" in Present Management
    assert presents["P001"]["status"] == "assigned"
    assert presents["P002"]["status"] == "assigned"

    # AND: No duplicate assignments occur
    assert len(busy_elves) == 2
    assert busy_elves == {"E001": "P001", "E002": "P002"}

    # AND: Both elves are removed from available_elves
    assert "E001" not in available_elves
    assert "E002" not in available_elves
    assert len(available_elves) == 0


# Story ID: SCHEDULING-INFRA-001.1
# Scenario ID: SCHEDULING-INFRA-001.1-S1


def test_scheduling_infra_001_1_s1_concurrent_assignments():
    # GIVEN: The available_elves set contains elves "E001" and "E002"
    available_elves.clear()
    available_elves.update(["E001", "E002"])

    # AND: The busy_elves dictionary is empty
    busy_elves.clear()

    # AND: Present "P001" and "P002" are available from Present Management
    presents.clear()
    presents["P001"] = {
        "present_id": "P001",
        "family_id": "F001",
        "status": "available",
    }
    presents["P002"] = {
        "present_id": "P002",
        "family_id": "F002",
        "status": "available",
    }

    # Track exceptions raised in worker threads
    exceptions = []

    # Track successful assignments
    assignments = []
    assignments_lock = threading.Lock()

    # Worker function: concurrent assignment calls for different elves
    def assignment_worker(present_id, elf_id):
        try:
            barrier.wait(timeout=5.0)
            result = assign_present_to_elf(present_id=present_id, elf_id=elf_id)
            with assignments_lock:
                assignments.append(result)
        except Exception as e:
            exceptions.append(e)

    # Use barrier to synchronize both threads
    barrier = threading.Barrier(2)

    # Create threads that request DIFFERENT elves concurrently
    thread_a = threading.Thread(
        target=assignment_worker, args=("P001", "E001"), name="Thread-A"
    )
    thread_b = threading.Thread(
        target=assignment_worker, args=("P002", "E002"), name="Thread-B"
    )

    thread_a.start()
    thread_b.start()

    thread_a.join(timeout=5.0)
    thread_b.join(timeout=5.0)

    # AND: Both threads completed without exceptions
    assert not thread_a.is_alive(), "Thread-A did not complete"
    assert not thread_b.is_alive(), "Thread-B did not complete"
    assert len(exceptions) == 0, f"Unexpected exceptions: {exceptions}"

    # THEN: Both assignments are non-None and match exact expected mappings
    assert (
        len(assignments) == 2
    ), f"Expected 2 successful assignments, got {len(assignments)}: {assignments}"

    # E001 -> P001
    assignment_e001_p001 = next(
        (a for a in assignments if a["elf_id"] == "E001" and a["present_id"] == "P001"),
        None,
    )
    assert assignment_e001_p001 is not None, "E001 -> P001 assignment not found"

    # E002 -> P002
    assignment_e002_p002 = next(
        (a for a in assignments if a["elf_id"] == "E002" and a["present_id"] == "P002"),
        None,
    )
    assert assignment_e002_p002 is not None, "E002 -> P002 assignment not found"

    # AND: E001 is in busy_elves with present P001
    assert "E001" in busy_elves
    assert busy_elves["E001"] == "P001"

    # AND: E002 is in busy_elves with present P002
    assert "E002" in busy_elves
    assert busy_elves["E002"] == "P002"

    # AND: Both presents are marked as "assigned"
    assert presents["P001"]["status"] == "assigned"
    assert presents["P002"]["status"] == "assigned"

    # AND: No race condition corrupts available_elves state (both moved to busy)
    assert len(available_elves) == 0
    assert "E001" not in available_elves
    assert "E002" not in available_elves


# Story ID: SCHEDULING-STORY-001
# Scenario ID: SCHEDULING-STORY-001-S3


def test_scheduling_story_001_s3_cross_component_concurrent_operations():
    # GIVEN: Present "P001" is in the "available" status in Present Management
    # inventory
    presents.clear()
    family_groups.clear()

    presents["P001"] = {
        "present_id": "P001",
        "family_id": "F001",
        "status": "available",
    }

    # AND: Elf "E001" is in the `available_elves` set in Delivery Scheduling
    available_elves.clear()
    available_elves.add("E001")

    # AND: The `busy_elves` dictionary is empty
    busy_elves.clear()

    # Track exceptions raised in worker threads
    exceptions = []

    # Track assignment result
    assignment_result = []
    assignment_lock = threading.Lock()

    # WHEN: Mrs Claus calls assign_present_to_elf while Present Management
    # processes receive_present
    def assignment_worker():
        try:
            barrier.wait(timeout=5.0)
            result = assign_present_to_elf(present_id="P001", elf_id="E001")
            with assignment_lock:
                assignment_result.append(result)
        except Exception as e:
            exceptions.append(e)

    def present_arrival_worker():
        try:
            barrier.wait(timeout=5.0)
            receive_present(present_id="P002", family_id="F002")
        except Exception as e:
            exceptions.append(e)

    # Use barrier to synchronize both threads
    barrier = threading.Barrier(2)

    # Create threads for concurrent operations
    thread_a = threading.Thread(target=assignment_worker, name="Thread-A")
    thread_b = threading.Thread(target=present_arrival_worker, name="Thread-B")

    thread_a.start()
    thread_b.start()

    thread_a.join(timeout=5.0)
    thread_b.join(timeout=5.0)

    # THEN: Both threads completed without exceptions
    assert not thread_a.is_alive(), "Thread-A did not complete"
    assert not thread_b.is_alive(), "Thread-B did not complete"
    assert len(exceptions) == 0, f"Unexpected exceptions: {exceptions}"

    # AND: Elf "E001" receives present "P001" (atomic assignment)
    assert len(assignment_result) == 1
    assert assignment_result[0] == {"elf_id": "E001", "present_id": "P001"}

    # AND: Present "P002" is added to inventory without conflict
    assert "P002" in presents
    assert presents["P002"]["present_id"] == "P002"
    assert presents["P002"]["family_id"] == "F002"
    assert presents["P002"]["status"] == "available"

    # AND: E001 is moved to busy_elves
    assert "E001" in busy_elves
    assert busy_elves["E001"] == "P001"

    # AND: E001 is removed from available_elves
    assert "E001" not in available_elves

    # AND: Present "P001" is marked assigned
    assert presents["P001"]["status"] == "assigned"

    # AND: Family group for F002 contains P002
    assert "F002" in family_groups
    assert "P002" in family_groups["F002"]

    # AND: No race condition corrupts state
    # Verify final state consistency
    assert len(presents) == 2
    assert presents["P001"]["status"] == "assigned"
