# 4. Solution Strategy

## 4.1 Architectural Approach

The Christmas Delivery system follows a **modular monolith** architecture. All components run within a single Python process, communicate through well-defined interfaces, and share an in-memory data store. This approach provides clear separation of responsibilities while keeping deployment and development simple.

### Key Principles

| Principle | Rationale |
|---|---|
| **Single process execution** | Current implementation choice. Simplifies development, testing, and deployment. No network communication required between components. |
| **Clear component boundaries** | Each component has a single responsibility. This supports independent testing and future maintenance. |
| **Shared in-memory state** | All components access the same data store. Synchronization mechanisms handle concurrent access. |
| **Python 3.12 without an additional application framework** | Core implementation relies on the Python standard library. Third-party development or testing libraries may be used if beneficial. |

## 4.2 Technology Strategy

### Python 3.12 without Application Framework

The system uses Python 3.12 without an additional application framework. This decision:

- **Eliminates overhead** of framework-specific patterns and conventions
- **Simplifies learning** for TDD/BDD exercises
- **Focuses attention** on core domain logic and concurrent behavior
- **Enables full control** over data structures and component interfaces

Third-party testing or development libraries are not prohibited but are not required for the core implementation.

### In-Memory Data Management

All domain data (presents, families, elves, sleigh state) is stored in Python data structures:

- **Dictionaries** for quick lookups (family ID → presents, elf ID → assignment)
- **Lists/queues** for ordered processing (waiting presents, sleigh queue)
- **Thread-safe primitives** for concurrent access (locks, events, conditions)

Data is not persisted across application runs. The application starts with an empty state each time.

## 4.3 Component Responsibilities

### Present Management

**Responsibilities:**

- Present reception from toy machines
- Present tracking and inventory
- Family grouping
- Cancellation handling
- Present availability status

**Key operations:**

- `receive_present(present_id, family_id)` - Add new present to inventory
- `cancel_family_presents(family_id)` - Mark all family presents as cancelled
- `get_available_presents()` - Return unassigned presents
- `group_presents_by_family()` - Group presents for efficient delivery

### Delivery Scheduling

**Responsibilities:**

- Mrs Claus's coordination logic
- Elf assignment
- Scheduling decisions (when to assign, when to wait)
- Present holding when no elves available

**Key operations:**

- `assign_presents_to_elves()` - Match available presents to available elves
- `hold_present(present)` - Store present until an elf becomes available
- `release_held_present()` - Deliver held present to available elf

### Sleigh Management

**Responsibilities:**

- Sleigh loading operations
- Elf assignment completion tracking

**Key operations:**

- `load_present(present, elf_id)` - Record present loading onto sleigh by elf
- `elf_assignment_completed(elf_id)` - Mark elf as available after completing delivery

## 4.4 Concurrency Strategy

### Concurrent Elf Assignment

Multiple elves may request presents simultaneously. The architecture supports this through:

- **Thread-safe data structures** for shared state
- **Locking mechanisms** to prevent race conditions
- **Atomic operations** for present assignment

### Shared-State Synchronization

Present Management maintains a shared state accessed by Delivery Scheduling and Sleigh Management. Synchronization ensures:

- **No duplicate assignments** of the same present to multiple elves
- **Accurate inventory counts** during concurrent operations
- **Consistent state** during family grouping and cancellation

### Conflict Resolution

When conflicts arise (e.g., simultaneous cancellation and assignment):

- **Unresolved design detail:** The original kata does not define cancellation behavior for presents already being processed.
- Potential approaches: Cancellation takes priority, or assignment completes first.
- Implementation decision to be determined based on requirements clarification.

## 4.5 Trade-Offs and Rationale

### Modular Monolith vs. Microservices

| Factor | Modular Monolith | Microservices |
|---|---|---|
| **Complexity** | Lower for small-to-medium systems | Higher due to network, deployment complexity |
| **Development speed** | Faster initial development | May be slower due to service coordination |
| **Scalability** | Limited by single process | Can scale independently, but with overhead |
| **Fault isolation** | Limited—failures may affect all components | Better isolation between services |

**Decision:** Modular monolith is appropriate for this kata. The system doesn't require independent scaling or fault isolation. Simplicity and clarity are prioritized.

### In-Memory Storage vs. Database

| Factor | In-Memory | Database |
|---|---|---|
| **Development speed** | Faster—no schema or migrations | Slower—DB setup required |
| **Persistence** | None—data lost on restart | Data survives restart |
| **Scalability** | Limited by memory size | Can scale with database infrastructure |

**Decision:** In-memory storage is sufficient for this simulation. Persistence is not a requirement. The system demonstrates architectural patterns without infrastructure complexity.

### Single Process vs. Distributed

| Factor | Single Process | Distributed |
|---|---|---|
| **Deployment** | Simple—single application | Complex—multiple services |
| **Communication** | Direct method calls | Network calls, serialization |
| **Testing** | Easier—direct component calls | Harder—mock services required |

**Decision:** Single process aligns with modular monolith and in-memory constraints. The kata focuses on component architecture, not distributed systems.

## 4.6 Alignment with User Stories

| User Story | Supporting Architecture |
|---|---|
| **US-1** Elf takes presents from toy machine and packs onto sleigh | Sleigh Management + Delivery Scheduling coordination |
| **US-2** Mrs Claus receives presents, assigns elves, holds when no elves | Delivery Scheduling with hold mechanism |
| **US-3** Presents grouped by family, arrivals interleaved | Present Management family grouping |
| **US-4** Santa requests cancellation, Mrs Claus discards | Present Management + Cancellation handler |
