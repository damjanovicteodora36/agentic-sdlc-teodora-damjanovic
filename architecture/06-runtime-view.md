# 6. Runtime View

## 6.1 Overview

The runtime view describes how the three components interact during key scenarios defined by the original kata user stories. The components communicate through method calls within a single Python process. Shared state is protected with synchronization primitives to handle concurrent access.

## 6.2 User Story 1: Single Elf Packing

A present arrives and is assigned to an available elf, who loads it onto Santa's sleigh.

### Participants

| Component | Role |
|---|---|
| Present Management | Provides available presents |
| Delivery Scheduling | Assigns present to available elf and owns elf availability |
| Sleigh Management | Records completed loading operations |

### Interaction Steps

1. **Toy Machine supplies present** → `Present Management.receive_present(present_id, family_id)`
   - Present Management adds present to inventory
   - Family grouping updated if family already exists

2. **Delivery Scheduling requests available presents** → `Present Management.get_available_presents()`
   - Present Management returns unassigned presents

3. **Delivery Scheduling assigns present to elf** → `Delivery Scheduling.assign_present_to_elf(present, elf_id)`
   - Delivery Scheduling marks elf as unavailable and records the active assignment
   - This step is the assignment; the elf performs the packing/loading operation

4. **Delivery Scheduling requests present loading** → `Sleigh Management.load_present(present_id, elf_id)`
   - Sleigh Management records present loading onto sleigh

5. **Elf completes loading operation** → `Sleigh Management.elf_assignment_completed(elf_id)`
   - Sleigh Management reports completion via callback to Delivery Scheduling

6. **Delivery Scheduling marks elf as available** → `Delivery Scheduling.mark_elf_available(elf_id)`
   - Delivery Scheduling removes elf from busy assignments and returns to `available_elves`

### State Changes

| Component | State Change |
|---|---|
| Present Management | Present marked as assigned (not returned to `get_available_presents()`) |
| Delivery Scheduling | Elf moved from `available_elves` to `busy_elves`, then back to `available_elves` after completion |
| Sleigh Management | Present added to `loaded_presents` |

## 6.3 User Story 2: Hold and Assign When Elf Available

Presents are held when no elves are available and assigned when an elf becomes free.

### Participants

| Component | Role |
|---|---|
| Present Management | Provides available presents |
| Delivery Scheduling | Holds presents when no elves available, then assigns when elf available |
| Sleigh Management | Reports elf completion via callback |

### Interaction Steps (No Elf Available)

1. **Toy Machine supplies present** → `Present Management.receive_present(present_id, family_id)`
2. **Delivery Scheduling requests available presents** → `Present Management.get_available_presents()`
3. **Delivery Scheduling checks for available elves** → `Delivery Scheduling.get_available_elves()`
4. **No elves available** → `Delivery Scheduling.hold_present(present)`
   - Present stored in `held_presents` list

### Interaction Steps (Elf Becomes Available)

5. **Elf completes loading operation** → `Sleigh Management.elf_assignment_completed(elf_id)`
6. **Delivery Scheduling marks elf as available** → `Delivery Scheduling.mark_elf_available(elf_id)`
7. **Delivery Scheduling processes held presents** → `Delivery Scheduling.assign_held_presents()`
   - A selected held present is assigned to the newly available elf
   - The elf receives the assignment, performs the loading onto the sleigh, Sleigh Management records the completion and sends a notification, and Delivery Scheduling marks the elf available again

### State Changes

| Component | State Change |
|---|---|
| Delivery Scheduling | Present moved from `held_presents` to active assignment |

## 6.4 User Story 3: Family Grouping with Minimized Idle Time

Presents are grouped by family when possible, while minimizing elf idle time.

### Participants

| Component | Role |
|---|---|
| Present Management | Groups presents by family |
| Delivery Scheduling | Balances family grouping against minimizing elf idle time |

### Interaction Steps

1. **Multiple presents arrive for same family** → `Present Management.receive_present()` called multiple times
2. **Present Management groups presents** → Family grouping maintained in `family_groups` dictionary
3. **Delivery Scheduling requests available presents** → `Present Management.get_available_presents()`
4. **Delivery Scheduling optimizes assignment order** (implementation detail)
   - Scheduling objective: group presents by family where possible
   - Scheduling objective: minimize elf idle time
   - No specific algorithm prescribed; balance determined during implementation
5. **Assignment proceeds as User Story 1 or User Story 2**

### State Changes

| Component | State Change |
|---|---|
| Present Management | Family group updated when new present arrives |
| Delivery Scheduling | Assignment order optimized for family grouping |

## 6.5 User Story 4: Cancellation Handling

Santa requests cancellation of presents for a family.

### Participants

| Component | Role |
|---|---|
| Present Management | Handles cancellation request |
| Delivery Scheduling | Updates assignment eligibility for cancelled family |

### Interaction Steps

1. **Santa requests cancellation** → `Present Management.cancel_family_presents(family_id)`
2. **Present Management marks all pending family presents as cancelled**
   - Removed from available presents
   - Removed from family groups
   - Added to `cancelled_families` set

3. **Delivery Scheduling updates assignment eligibility** (unresolved design detail)
   - **Unresolved:** Original kata does not define cancellation behavior for presents already assigned to elves
   - Pending presents (in `held_presents` or available pool) must no longer be eligible for assignment
   - Behavior for already-assigned presents remains unresolved

### State Changes

| Component | State Change |
|---|---|
| Present Management | Family presents marked as cancelled |
| Delivery Scheduling | Pending presents from cancelled family excluded from assignment |

## 6.6 Concurrency and Consistency Requirements

### Thread Safety

- **Shared state** across components requires thread-safe access
- **Write operations** to shared state must be protected
- **Read operations** may require consistency guarantees

### Conflict Resolution

- **Race conditions**: Prevent duplicate assignment of same present to multiple elves
- **Cancellation vs assignment**: Unresolved behavior for presents already assigned when cancellation requested

### Synchronization Implementation

- Locks, conditions, queues, or other primitives will be determined during implementation
- No specific synchronization strategy prescribed at architecture level
