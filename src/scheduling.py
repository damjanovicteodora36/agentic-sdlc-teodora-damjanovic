"""Delivery Scheduling component."""

from src.present_management import presents

available_elves = set()
busy_elves = {}


def assign_present_to_elf(present_id: str, elf_id: str):
    """Assign a present to an elf."""
    # Move elf from available to busy
    available_elves.discard(elf_id)
    busy_elves[elf_id] = present_id

    # Update present status to assigned
    if present_id in presents:
        presents[present_id]["status"] = "assigned"

    # Return assignment record
    return {"elf_id": elf_id, "present_id": present_id}
