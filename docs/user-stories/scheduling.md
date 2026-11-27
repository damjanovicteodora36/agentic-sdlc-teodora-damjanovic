# SCHEDULING Domain User Stories

## SCHEDULING-STORY-001

**Parent Story ID**: SCHEDULING-STORY-001
**Parent Story**: AS A Mrs Claus I WANT to assign presents to available elves SO THAT I can coordinate the delivery workflow

### SCENARIO 1: Mrs Claus assigns available present to available elf

**Scenario ID**: SCHEDULING-STORY-001-S1

**GIVEN**
* Present "P001" for family "F001" is in the "available" status in Present Management inventory
* Elf "E001" is in the `available_elves` set owned by Delivery Scheduling
* The `busy_elves` dictionary in Delivery Scheduling is empty

**WHEN**
* Mrs Claus calls `assign_present_to_elf(present_id="P001", elf_id="E001")`

**THEN**
* Elf "E001" is moved from `available_elves` to `busy_elves` in Delivery Scheduling
* The active assignment "E001" → "P001" is recorded in Delivery Scheduling
* The present "P001" status is updated to "assigned" in Present Management
* The assignment is returned to Sleigh Management for loading

### SCENARIO 2: Mrs Claus assigns multiple presents to multiple available elves

**Scenario ID**: SCHEDULING-STORY-001-S2

**GIVEN**
* Present "P001" and "P002" are in the "available" status in Present Management inventory
* Elf "E001" and "E002" are in the `available_elves` set in Delivery Scheduling
* The `busy_elves` dictionary is empty

**WHEN**
* Mrs Claus calls `assign_present_to_elf(present_id="P001", elf_id="E001")` and `assign_present_to_elf(present_id="P002", elf_id="E002")`

**THEN**
* Elf "E001" receives present "P001" and is moved to `busy_elves`
* Elf "E002" receives present "P002" and is moved to `busy_elves`
* Both presents are marked as "assigned" in Present Management
* No duplicate assignments occur

### SCENARIO 3: Concurrent present and elf availability checks

**Scenario ID**: SCHEDULING-STORY-001-S3

**GIVEN**
* Present "P001" is in the "available" status in Present Management inventory
* Elf "E001" is in the `available_elves` set in Delivery Scheduling
* Multiple simultaneous requests arrive: Mrs Claus requests assignment for "P001" and a new present "P002" arrives

**WHEN**
* Mrs Claus calls `assign_present_to_elf(present_id="P001", elf_id="E001")` while Present Management processes `receive_present(present_id="P002", family_id="F002")`

**THEN**
* Elf "E001" receives present "P001" (atomic assignment)
* Present "P002" is added to inventory without conflict
* No race condition corrupts elf availability or present status

## Architecture References

- Delivery Scheduling: Section 5.2 (elf availability, active assignments)
- Present Management: Section 5.2 (available presents, status updates)
- Sleigh Management: Section 5.2 (loading operations)
- Concurrency: Section 4.4, NFR-01, NFR-02
- Constraints: Section 2.1, 2.2, 2.3
- Quality Scenarios: QS-01 (Consistent State), QS-02 (Family Grouping Accuracy)

## Original Kata Requirements

- **US-1**: A single elf takes presents from a toy machine and packs them onto Santa's sleigh
- **US-2**: Mrs Claus receives presents from multiple toy machines and assigns them to available elves
- **FR-02**: Mrs Claus assigns presents to available elves

## Domain: SCHEDULING

## Backend Sub-stories

### SCHEDULING-BE-001.1

**Parent Story ID**: SCHEDULING-STORY-001
**Story Type**: Backend
**Parent Story**: AS A Delivery Scheduling Component I WANT to track elf availability and assignments SO THAT Mrs Claus can coordinate present delivery

### SCENARIO 1: Record elf assignment when both present and elf available

**Scenario ID**: SCHEDULING-BE-001.1-S1

**GIVEN**
* The `available_elves` set contains elf "E001"
* The `busy_elves` dictionary is empty
* Present "P001" is available from Present Management

**WHEN**
* `assign_present_to_elf(present_id="P001", elf_id="E001")` is called

**THEN**
* Elf "E001" is removed from `available_elves`
* Elf "E001" is added to `busy_elves` with value "P001"
* The assignment record is returned for Sleigh Management

### SCHEDULING-BE-001.2

**Parent Story ID**: SCHEDULING-STORY-001
**Story Type**: Backend
**Parent Story**: AS A Concurrent Assignment Component I WANT multiple elf assignments to be processed correctly SO THAT no elves receive duplicate presents

### SCENARIO 1: Atomic availability check and assignment

**Scenario ID**: SCHEDULING-BE-001.2-S1

**GIVEN**
* The `available_elves` set contains elves "E001" and "E002"
* Mrs Claus / Delivery Scheduling simultaneously processes multiple assignment requests
* The assignment interface requires atomic availability check and assignment

**WHEN**
* Mrs Claus calls `assign_present_to_elf(present_id="P001", elf_id="E001")` and `assign_present_to_elf(present_id="P002", elf_id="E002")` concurrently

**THEN**
* Each elf receives a unique present (no duplicates)
* The availability check and assignment are atomic
* No race condition corrupts the `available_elves` state

## Infrastructure Sub-stories

### SCHEDULING-INFRA-001.1

**Parent Story ID**: SCHEDULING-STORY-001
**Story Type**: Infrastructure
**Parent Story**: AS A Thread-Safe State Component I WANT elf availability and assignments to be thread-safe SO THAT concurrent assignment requests from Mrs Claus do not cause race conditions

### SCENARIO 1: Thread-safe assignment when Mrs Claus processes multiple requests simultaneously

**Scenario ID**: SCHEDULING-INFRA-001.1-S1

**GIVEN**
* The `available_elves` set contains elves "E001" and "E002"
* Mrs Claus simultaneously processes multiple assignment requests
* The assignment interface requires atomic availability check and assignment

**WHEN**
* Mrs Claus calls `assign_present_to_elf(present_id="P001", elf_id="E001")` and `assign_present_to_elf(present_id="P002", elf_id="E002")` concurrently

**THEN**
* Each elf receives a unique present (no duplicates)
* The availability check and assignment are atomic
* No race condition corrupts the `available_elves` state

### SCHEDULING-INFRA-001.2

**Parent Story ID**: SCHEDULING-STORY-001
**Story Type**: Infrastructure
**Parent Story**: AS A Present Availability Interface I WANT Delivery Scheduling to query available presents from Present Management SO THAT Mrs Claus can assign them to elves

**Note**: Integration concern — describes internal component communication in the single-process modular monolith

### SCENARIO 1: Query available presents from Present Management

**Scenario ID**: SCHEDULING-INFRA-001.2-S1

**GIVEN**
* Present Management maintains the `presents` dictionary with available and assigned presents
* Delivery Scheduling needs presents for assignment

**WHEN**
* `get_available_presents()` is called on Present Management

**THEN**
* Only presents with status "available" are returned
* Assigned presents are excluded from the result

### SCHEDULING-INFRA-001.3

**Parent Story ID**: SCHEDULING-STORY-001
**Story Type**: Infrastructure
**Parent Story**: AS A Component Communication Interface I WANT Sleigh Management to notify Delivery Scheduling when elves complete assignments SO THAT elves can receive new presents

**Note**: Integration concern — describes internal component communication in the single-process modular monolith

### SCENARIO 1: Notify Delivery Scheduling when elf completes loading

**Scenario ID**: SCHEDULING-INFRA-001.3-S1

**GIVEN**
* Elf "E001" has completed loading present "P001" onto the sleigh
* Sleigh Management has called `elf_assignment_completed(elf_id="E001")`

**WHEN**
* Delivery Scheduling receives the completion notification

**THEN**
* Elf "E001" is removed from `busy_elves`
* Elf "E001" is added to `available_elves`
* The completion is processed for next assignment cycle

**Shared Docker CI/testing infrastructure:** The Docker build and test execution requirements defined in PRESENT-INFRA-001.5 and PRESENT-INFRA-001.6 apply to the entire Python modular monolith, including the SCHEDULING component. Both domains share the Dockerfile and CI pipeline introduced in Module 4. No additional Docker service or separate SCHEDULING Docker configuration is required.

## Frontend (Not Applicable)

**Note**: This Python modular monolith architecture does not include a graphical frontend. All user stories are implemented as internal component interfaces within the single Python process. Elf assignment is triggered by:
- Mrs Claus simulation code (external system simulation)
- Test code calling assignment methods directly
- Integration scripts managing the delivery workflow

The component interface `assign_present_to_elf(present_id, elf_id)` serves as the "user story implementation" for the SCHEDULING component.
