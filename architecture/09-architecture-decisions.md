# 9. Architecture Decisions

## ADR-001: Technology Stack and Architectural Style

**Status:** Accepted

### Context

The Christmas Delivery kata simulates the production and
delivery of presents by toy machines and delivery elves.

The system must support present management, elf assignment,
family grouping, and cancellation of presents.

The architecture should remain simple while providing clear
separation of responsibilities and support for concurrent
processing.

### Decision

The following technology choices have been made:

- **Programming Language:** Python 3.12
- **Framework:** Python standard library, without an additional
  application framework
- **Data Storage:** In-memory data structures
- **Architectural Style:** Modular monolith

The application will be organized into three main components:

1. Present Management
2. Delivery Scheduling
3. Sleigh Management

### Rationale

Python 3.12 provides built-in data structures and concurrency
mechanisms suitable for implementing the kata.

An additional framework is unnecessary because the kata does
not require a web interface or external API.

In-memory storage is sufficient for managing presents, family
groups, and delivery queues during a simulation.

A modular monolith keeps deployment and development simple
while allowing responsibilities to be separated into
independent components.

### Consequences

**Positive:**
- Simple development and testing environment.
- No additional framework or database configuration.
- Clear separation of responsibilities.
- Suitable foundation for future TDD and BDD exercises.

**Negative:**
- Data is lost when the application terminates.
- Scaling across multiple processes would require additional
  coordination mechanisms.
- In-memory state requires synchronization when accessed
  concurrently.

The architecture may be reconsidered if future requirements
introduce persistent storage or distributed execution.
