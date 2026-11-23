# 12. Glossary

## Domain Terms

| Term | Definition |
|---|---|
| **Present** | An item produced by toy machines that belongs to a family and is packed onto Santa's sleigh. The Christmas Delivery system manages present reception, tracking, assignment, and cancellation. |
| **Toy Machine** | External system that produces presents for different families and supplies them to the Christmas Delivery system. |
| **Elf** | External actor (Delivery Elf) who takes presents from the system, loads them onto Santa's sleigh, and becomes available again after completing the operation. |
| **Mrs Claus** | External actor who coordinates present distribution by assigning presents to available elves. |
| **Santa Claus** | External actor who may request cancellation of presents for families. |
| **Santa's Sleigh** | External system that receives packed presents from elves for delivery to families. |
| **Family Grouping** | Arrangement of presents by family ID to optimize delivery efficiency. |
| **Held Present** | A present that has been received but not yet assigned to an elf because no elves were available. |
| **Present Assignment** | The process of matching an available present to an available elf for loading onto Santa's sleigh. |
| **Present Cancellation** | The process of marking all pending presents for a family as cancelled, excluding them from future assignments. Behavior for already-assigned presents remains unresolved. |

## Architectural Terms

| Term | Definition |
|---|---|
| **Modular Monolith** | A single deployable application with clearly separated internal modules. Single-process execution is our chosen implementation approach, not an inherent requirement of every modular monolith. |
| **Component** | A distinct part of the system with a single responsibility and well-defined interfaces (Present Management, Delivery Scheduling, Sleigh Management). |
| **C4 Model** | A hierarchical modeling language for describing software architecture at different levels of abstraction (Context, Container, Component, Code). |
| **In-Memory Storage** | Data storage mechanism using Python data structures (dictionaries, lists) within a single process, with no persistence across application runs. |
| **Shared State** | Data that is accessed and modified by multiple components within the same process, requiring synchronization for consistency. |
| **Concurrency** | The ability of operations to overlap in time or have interleaved execution, without necessarily running simultaneously on separate processors. |
| **Synchronization** | Mechanisms (locks, conditions, queues, or other primitives) used to ensure thread-safe access to shared state. |
| **Atomic Operation** | An operation that appears to the rest of the system as a single, indivisible action, preventing race conditions. |
| **ADR** | Architectural Decision Record, a document that captures an architectural decision, its context, rationale, and consequences. |
| **arc42** | A template for documenting software architecture, consisting of 12 chapters covering different aspects of the architecture. |

## Unresolved Terms

| Term | Status |
|---|---|
| **Cancellation of Assigned Presents** | Behavior for presents already assigned to elves when cancellation is requested. Not defined in original kata. Implementation decision pending. |
