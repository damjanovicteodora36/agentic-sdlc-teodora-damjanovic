"""Delivery Scheduling component."""

import threading

from src.present_management import presents

available_elves = set()
busy_elves = {}
_lock = threading.Lock()


def assign_present_to_elf(present_id: str, elf_id: str):
    """Assign a present to an elf atomically.

    Returns the assignment dict if successful, None if the elf is unavailable.
    """
    with _lock:
        # Check if elf is available
        if elf_id not in available_elves:
            return None

        # Remove elf from available and add to busy
        available_elves.discard(elf_id)
        busy_elves[elf_id] = present_id

        # Update present status to assigned
        if present_id in presents:
            presents[present_id]["status"] = "assigned"

        # Return assignment record
        return {"elf_id": elf_id, "present_id": present_id}


def elf_assignment_completed(elf_id: str) -> None:
    """Process elf completion of assignment.

    Removes elf from busy_elves and adds back to available_elves.
    Uses thread-safe locking for state transitions.
    """
    with _lock:
        # Remove elf from busy_elves
        if elf_id in busy_elves:
            del busy_elves[elf_id]

        # Add elf back to available_elves
        available_elves.add(elf_id)
