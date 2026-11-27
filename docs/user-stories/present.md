# PRESENT Domain User Stories

## PRESENT-STORY-001

**Parent Story ID**: PRESENT-STORY-001
**Parent Story**: AS A Toy Machine I WANT the system to receive presents from me SO THAT Mrs Claus can assign them to elves for delivery

### SCENARIO 1: Toy machine supplies present with family ID

**Scenario ID**: PRESENT-STORY-001-S1

**GIVEN**
* The system has been initialized with an empty present inventory
* Toy Machine is ready to supply a present
* The present belongs to a valid family (family_id is provided)

**WHEN**
* Toy Machine calls `receive_present(present_id="P001", family_id="F001")`

**THEN**
* The present record is added to the in-memory inventory with ID "P001" and family_id "F001"
* The present status is set to "available"
* The family group for "F001" is created or updated to include present "P001"
* No duplicate present with ID "P001" exists in the inventory

### SCENARIO 2: Toy machine supplies multiple presents for same family

**Scenario ID**: PRESENT-STORY-001-S2

**GIVEN**
* The system has been initialized with an empty present inventory
* Present "P001" for family "F001" already exists in inventory

**WHEN**
* Toy Machine calls `receive_present(present_id="P002", family_id="F001")`

**THEN**
* Present "P002" is added to the inventory with family_id "F001"
* The family group for "F001" now includes both "P001" and "P002"
* Present "P001" remains in "available" status

### SCENARIO 3: Concurrent present arrivals from multiple toy machines

**Scenario ID**: PRESENT-STORY-001-S3

**GIVEN**
* The system has been initialized with an empty present inventory
* Multiple toy machines are simultaneously preparing presents

**WHEN**
* Toy Machine A calls `receive_present(present_id="P001", family_id="F001")` at the same time as Toy Machine B calls `receive_present(present_id="P002", family_id="F002")`

**THEN**
* Present "P001" is added to inventory with family_id "F001"
* Present "P002" is added to inventory with family_id "F002"
* No race condition occurs
* The inventory accurately reflects both presents

## Architecture References

- Present Management: Section 5.2
- Delivery Scheduling: Section 5.2 (dependencies on Present Management)
- Concurrency: Section 4.4, NFR-01, NFR-02
- Constraints: Section 2.1, 2.2, 2.3
- Quality Scenarios: QS-01 (Consistent State), QS-02 (Family Grouping Accuracy)

## Original Kata Requirements

- **US-1**: A single elf takes presents from a toy machine and packs them onto Santa's sleigh
- **US-2**: Mrs Claus receives presents from multiple toy machines and assigns them to available elves
- **FR-01**: Toy machines supply presents to the system

## Domain: PRESENT

## Backend Sub-stories

### PRESENT-BE-001.1

**Parent Story ID**: PRESENT-STORY-001
**Story Type**: Backend
**Parent Story**: AS A Delivery Scheduling Component I WANT presents to be stored in the system SO THAT Mrs Claus can assign them to elves

### SCENARIO 1: Store new present record

**Scenario ID**: PRESENT-BE-001.1-S1

**GIVEN**
* The system has been initialized with an empty present inventory data structure
* The present record structure (dict with present_id, family_id, status) is defined

**WHEN**
* `receive_present(present_id="P001", family_id="F001")` is called

**THEN**
* A new present record is created with fields: present_id="P001", family_id="F001", status="available"
* The record is stored in the `presents` dictionary with key "P001"
* The family group for "F001" is created in `family_groups` dict, and "P001" is added to the list

### PRESENT-BE-001.2

**Parent Story ID**: PRESENT-STORY-001
**Story Type**: Backend
**Parent Story**: AS A Concurrent Present Delivery Component I WANT multiple presents to be stored correctly SO THAT no presents are lost or duplicated

### SCENARIO 1: Concurrent present arrivals

**Scenario ID**: PRESENT-BE-001.2-S1

**GIVEN**
* The `receive_present` interface is implemented
* Multiple concurrent calls to `receive_present` are in progress

**WHEN**
* Two toy machines simultaneously call `receive_present` with different present IDs

**THEN**
* Both presents are added to the inventory without conflict
* The in-memory state remains consistent
* No duplicate entries or lost updates occur

## Infrastructure Sub-stories

### PRESENT-INFRA-001.1

**Parent Story ID**: PRESENT-STORY-001
**Story Type**: Infrastructure
**Parent Story**: AS A System Initialization Component I WANT the in-memory state structures to be ready SO THAT present reception can begin

### SCENARIO 1: Initialize in-memory state structures

**Scenario ID**: PRESENT-INFRA-001.1-S1

**GIVEN**
* The application starts and in-memory state must be initialized

**WHEN**
* The Christmas Delivery application initializes the Present Management component

**THEN**
* The `presents` dictionary is created (empty)
* The `family_groups` dictionary is created (empty)
* The `cancelled_families` set is created (empty)
* All data structures are ready for present reception

### PRESENT-INFRA-001.2

**Parent Story ID**: PRESENT-STORY-001
**Story Type**: Infrastructure
**Parent Story**: AS A Thread-Safe State Component I WANT present reception to be thread-safe SO THAT no race conditions occur during concurrent arrivals

### SCENARIO 1: Thread-safe access for concurrent arrivals

**Scenario ID**: PRESENT-INFRA-001.2-S1

**GIVEN**
* The shared in-memory data structures are initialized

**WHEN**
* `receive_present` is called from multiple threads simultaneously

**THEN**
* A threading.Lock or similar synchronization primitive protects write operations
* The present record is added atomically
* No race condition corrupts the state

### PRESENT-INFRA-001.3

**Parent Story ID**: PRESENT-STORY-001
**Story Type**: Infrastructure
**Parent Story**: AS A Monitoring Component I WANT present reception events to be logged SO THAT we can track delivery workflow

### SCENARIO 1: Log present reception events

**Scenario ID**: PRESENT-INFRA-001.3-S1

**GIVEN**
* Present reception operations occur during a delivery simulation

**WHEN**
* A present is successfully received by the system

**THEN**
* A log entry is written with structure: {"event": "present_received", "present_id": "<id>", "family_id": "<family_id>"}
* The log uses Python logging module with appropriate level (INFO)

### PRESENT-INFRA-001.4

**Parent Story ID**: PRESENT-STORY-001
**Story Type**: Infrastructure
**Parent Story**: AS A Developer I WANT the application to be packaged as an importable Python module SO THAT it can be executed and tested using standard Python tools

### SCENARIO 1: Package application as importable module for modular monolith execution

**Scenario ID**: PRESENT-INFRA-001.4-S1

**GIVEN**
* The application uses Python 3.12 standard library only (no external dependencies per architecture constraint)
* The project directory structure follows Python packaging conventions
* The application runs as a single-process modular monolith without network services

**WHEN**
* Developer launches the Python 3.12 application through its documented entry point

**THEN**
* The module imports correctly without syntax errors
* The Present Management component initializes in-memory state structures (`presents`, `family_groups`, `cancelled_families`)
* The application starts successfully with all required components available for the delivery workflow
* No cloud infrastructure or external services are required—Docker is used for CI/testing packaging only, without changing the approved Python 3.12 modular monolith architecture

## Architecture References

- `architecture/02-constraints.md` — Section 2.1: Python 3.12 technology constraints
- `architecture/02-constraints.md` — Section 2.3: architectural constraints
- `architecture/04-solution-strategy.md` — Section 4.3: component responsibilities
- `architecture/07-deployment-view.md` — Section 7.1, 7.2: single-process execution model

## Frontend (Not Applicable)

**Note**: This Python modular monolith architecture does not include a graphical frontend. All user stories are implemented as internal component interfaces within the single Python process. Present reception is triggered by:
- Toy Machine simulation code (external system simulation)
- Test code calling `receive_present()` directly
- Integration scripts managing the delivery workflow

The component interface `receive_present(present_id, family_id)` serves as the "user story implementation" for the PRESENT component.
