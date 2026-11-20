# 7. Deployment View

## 7.1 Deployment Nodes

### Application Host

| Property | Value |
|---|---|
| **Node Type** | Single machine |
| **Runtime Environment** | Python 3.12 |
| **Execution Model** | Single process (current implementation decision) |
| **State Persistence** | None (in-memory only) |

## 7.2 Deployment Structure

The Christmas Delivery application is deployed as a single Python process on a machine with Python 3.12 installed. The application contains three internal components (Present Management, Delivery Scheduling, Sleigh Management) that share an in-memory data store. All components run within the same process and communicate through method calls.

## 7.3 Component Deployment

### Present Management

- **Location**: Embedded in Christmas Delivery application
- **Execution Context**: Single Python process
- **State**: In-memory data structures
- **Dependencies**: None (core component)

### Delivery Scheduling

- **Location**: Embedded in Christmas Delivery application
- **Execution Context**: Single Python process
- **State**: In-memory data structures (elf availability, active assignments)
- **Dependencies**: Present Management, Sleigh Management

### Sleigh Management

- **Location**: Embedded in Christmas Delivery application
- **Execution Context**: Single Python process
- **State**: In-memory data structures (loaded presents)
- **Dependencies**: Delivery Scheduling

## 7.4 Deployment Scenarios

### Development Deployment

- **Environment**: Developer machine
- **Python Version**: 3.12
- **Execution**: Command determined during implementation (e.g., `python main.py`)
- **State**: In-memory, lost on termination

### Test Deployment

- **Environment**: CI/CD pipeline or local test runner
- **Python Version**: 3.12
- **Execution**: Test runner invocation (e.g., `pytest`)
- **State**: In-memory, isolated per test run

## 7.5 Deployment Assumptions

| Assumption | Rationale |
|---|---|
| Python 3.12 available on host | Core technology constraint per ADR-001 |
| Single process execution | Current implementation decision for modular monolith |
| In-memory state | No persistence requirement per ADR-001 |
| External systems available | Toy Machines and Santa's Sleigh are accessible for simulation |
| No network communication required | Single process, no IPC needed |

## 7.6 Deployment Dependencies

| Dependency | Description |
|---|---|
| Python 3.12 runtime | Required for application execution |
| Python standard library | Used for threading, data structures, and other functionality (specific modules determined during implementation) |
| No external services | Application is self-contained |

## 7.7 Deployment Considerations

### Data Loss

- Application termination results in complete data loss
- No recovery mechanism for in-memory state
- Each application start begins with empty state

### Scaling

- No horizontal scaling supported (single process)
- No load balancing required
- No distributed state synchronization needed
