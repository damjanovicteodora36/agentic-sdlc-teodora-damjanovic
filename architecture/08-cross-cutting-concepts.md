# 8. Cross-cutting Concepts

## 8.1 In-Memory State Management

### State Ownership

| State Area | Owner Component | Description |
|---|---|---|
| Present records | Present Management | All present data including status (available, assigned, cancelled) |
| Family groups | Present Management | Mapping of family IDs to their presents |
| Cancelled families | Present Management | Set of family IDs with cancelled presents |
| Available elves | Delivery Scheduling | Set of elf IDs available for assignment |
| Active assignments | Delivery Scheduling | Mapping of elf IDs to present IDs |
| Held presents | Delivery Scheduling | List of presents waiting for elves |
| Loaded presents | Sleigh Management | List of presents loaded onto sleigh |

### State Access Patterns

- **Read operations**: Components access shared state through well-defined interfaces
- **Write operations**: Protected by synchronization primitives (locks, conditions)
- **Ownership enforcement**: Each state area has a single owner responsible for consistency

## 8.2 Concurrency and Synchronization

### Concurrency Requirements

| Scenario | Requirement |
|---|---|
| Multiple presents arriving simultaneously | State updates must be atomic |
| Multiple elves requesting presents | No duplicate assignment of same present |
| Cancellation during active assignment | Unresolved design detail |

### Synchronization Approach

- **Locks, conditions, or events** are possible synchronization mechanisms to coordinate access to shared state
- The specific synchronization strategy will be determined during implementation
- Present assignment must be atomic (availability check + assignment)

### Conflict Resolution

| Conflict | Resolution Strategy |
|---|---|
| Duplicate assignment attempt | Synchronization prevents concurrent modification |
| Cancellation of pending present | Present Management marks as cancelled, Delivery Scheduling excludes from assignment |
| Cancellation of assigned present | Unresolved; implementation decision pending |

## 8.3 Consistency Requirements

### Data Consistency

| Data Area | Consistency Requirement |
|---|---|
| Present status | Must reflect current state (available/assigned/cancelled) |
| Family grouping | Must accurately group presents by family ID |
| Elf availability | Must accurately track available vs busy elves |
| Sleigh loading | Must accurately record loaded presents |

### Invariants

| Invariant | Description |
|---|---|
| Unique assignment | A present cannot be assigned to multiple elves simultaneously |
| Status consistency | Present status matches actual state (available, assigned, cancelled) |
| Assignment tracking | Active assignments are tracked by Delivery Scheduling |
| Loaded records | All presents on sleigh are recorded by Sleigh Management |

## 8.4 Error Handling

### Error Types

| Error | Component | Handling Approach |
|---|---|---|
| Duplicate present ID | Present Management | Validation case (not specified in kata) |
| Invalid family ID | Present Management | Validation case (not specified in kata) |
| No elves available | Delivery Scheduling | Hold present until elf available (kata behavior) |

### Error Handling Strategy

- **Input validation**: Present Management validates present and family IDs
- **Graceful degradation**: Delivery Scheduling holds presents when no elves available
- **No explicit error handling**: Kata does not specify error behaviors beyond basic operations

## 8.5 Component Boundaries

### Interface Principles

| Component | Interface Type | Purpose |
|---|---|---|
| Present Management | Provider | Offers present data and cancellation interfaces |
| Delivery Scheduling | Coordinator | Uses Present Management and Sleigh Management interfaces |
| Sleigh Management | Consumer/Notifier | Records loading and reports completion |

### Boundary Enforcement

- **Direct method calls**: Components communicate through well-defined interfaces
- **No circular dependencies**: Delivery Scheduling uses interfaces from other components
- **State encapsulation**: Each component owns its state and provides controlled access

### Cross-Component Communication

| Communication | Direction | Description |
|---|---|---|
| Present availability request | Delivery Scheduling → Present Management | Get available presents for assignment |
| Present loading request | Delivery Scheduling → Sleigh Management | Request present loading onto sleigh |
| Completion notification | Sleigh Management → Delivery Scheduling | Report elf assignment completion via callback/interface |

## 8.6 Testability

### Testability Goals

| Goal | Support Mechanism |
|---|---|
| Component isolation | Each component has clear interfaces |
| State verification | In-memory state accessible for inspection |
| Concurrency testing | Synchronization primitives enable testing |
| Scenario simulation | External systems simulated through interfaces |

### Testing Support

- **Unit testing**: Each component can be tested with mock interfaces
- **Integration testing**: Components can be tested together with shared state
- **Concurrency testing**: Test scenarios with multiple presents and elves
- **State verification**: Inspect in-memory state after operations

### Test Infrastructure

- **Test runners**: pytest, unittest, or other Python testing frameworks
- **Mock objects**: Simulate Toy Machines, Santa's Sleigh, elves
- **State assertions**: Verify in-memory state after operations
