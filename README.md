# Agentic SDLC: Building a Software Factory

## About This Course

This course explores how to build a **software factory** — a collection of specialised AI agents that automate each stage of the software development lifecycle (SDLC). Rather than relying on a single general-purpose assistant, the software factory model assigns a dedicated agent to each discipline: architecture, requirements, testing, deployment, and more.

Each agent understands the conventions and artefacts of its domain, produces structured outputs, and hands off to the next agent in the pipeline. The result is a repeatable, auditable development process where AI handles the mechanical and formulaic work, freeing developers to focus on decisions that require judgement.

## How It Works

The SDLC is divided into stages, each owned by a specialised agent:

| Stage | Agent | Responsibility |
|---|---|---|
| Git Workflow | Git Workflow Agent | Issues, branches, commits, and pull requests |
| Architecture | Software Architecture Agent | arc42 documents and C4 diagrams |
| Requirements | Software Requirements Agent | User stories, DDD models, Pareto prioritisation |
| CI/CD | CI/CD Agent | GitHub Actions workflows and AWS SAM templates |
| Testing | TDD/BDD Multi-Agent System | Test writing, execution, implementation, and refactoring |
| Final Project | Integrated Pipeline | End-to-end software factory combining all agents |

Agents communicate through well-defined artefacts (files, structured outputs, GitHub Issues, and PRs), making the pipeline transparent and reproducible.

## Course Progress

- [x] Module 1: Git Workflow Agent
- [x] Module 2: Software Architecture Agent
- [x] Module 3: Software Requirements Agent
- [ ] Module 4: CI/CD Agent
- [ ] Module 5: TDD/BDD Multi-Agent System
- [ ] Module 6: Final Project

## Technology Stack

| Technology | Role |
|---|---|
| **Python 3.12** | Primary language for all agents and automation scripts |
| **React 18** | Frontend interface for interacting with the software factory |
| **GitHub Actions** | CI/CD pipeline execution and workflow automation |
| **pytest** | Unit and integration test runner |
| **pytest-bdd** | BDD scenario execution using Gherkin feature files |
| **Kiro CLI** | Agent orchestration, Git workflow automation, and template enforcement |
