# 2. Constraints

## 2.1 Technology Constraints

| Constraint | Impact | Source |
|---|---|---|
| **Python 3.12** | Must use Python 3.12 features and syntax. Code should be compatible with this version. | Technology choice from ADR-001 |
| **No application framework** | The application will use the Python standard library without an additional application framework. Third-party development and testing libraries are not prohibited. | Technology choice from ADR-001 |
| **In-memory data storage** | All present, family, elf, and sleigh data stored in Python data structures. No database persistence. | Technology choice from ADR-001 |

## 2.2 Business Constraints

| Constraint | Impact | Source |
|---|---|---|
| **Four user stories** | System must implement all four kata user stories exactly as specified. No additional features. | Original kata specification |
| **Elf availability model** | Elves must complete packing before becoming available again. No partial completion. | User Story 1 |
| **Mrs Claus coordination** | Mrs Claus must hold presents when no elves are available. No present loss. | User Story 2 |
| **Family grouping** | Present arrivals may be interleaved. Grouping should optimize elf utilization. | User Story 3 |
| **Cancellation handling** | Santa may request cancellation of presents for families. Mrs Claus discards these presents. | User Story 4 |

## 2.3 Architecture Constraints

| Constraint | Impact | Source |
|---|---|---|
| **Modular monolith** | All code in single repository. No microservices or external service calls. | Architecture choice from ADR-001 |
| **Three components** | Code organized into Present Management, Delivery Scheduling, and Sleigh Management components with clear boundaries. | Architecture choice from ADR-001 |
| **Component boundaries** | Components must have clear interfaces. Shared state requires synchronization for concurrent access. | Architecture choice from ADR-001 |

## 2.4 Development Constraints

| Constraint | Impact | Source |
|---|---|---|
| **TDD/BDD ready** | Architecture must support unit and integration testing. Components should be testable in isolation. | Architecture choice from ADR-001 |

## 2.5 External System Constraints

| System | Interface | Constraints |
|---|---|---|
| Toy Machines | Supplies presents | External; not part of our system |
| Santa's Sleigh | Receives packed presents | External; not part of our system |
| Santa (person) | Requests cancellations | External; not part of our system |
| Mrs Claus (person) | Coordinates deliveries | External; not part of our system |
