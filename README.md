# Local CLI Coder

Local CLI Coder is a self-directed project for learning Python by building a local coding agent from first principles.

The implementation is written manually by the learner. A Teacher Agent may inspect the work, run tests, and provide feedback, but it must not implement the assignment or change the learning plan.

## Progress

The checkboxes below are **teacher-verified major checkpoints**. They are updated only when the Teacher Agent reports `PASS` after running the required tests and checking the evidence in `Plan.md`.

| Status | Checkpoint | Milestone | Description |
|---|---|---|---|
| [ ] | MC-00 | 0 | Environment and Python Foundation |
| [ ] | MC-01 | 1 | CLI Skeleton |
| [ ] | MC-02 | 2 | Configuration and Logging |
| [ ] | MC-03 | 3 | Ollama Provider |
| [ ] | MC-04 | 4 | Tool Contract and Read-only Tools |
| [ ] | MC-05 | 5 | Agent Loop and State |
| [ ] | MC-06 | 6 | Context Management |
| [ ] | MC-07 | 7 | Patch and File Editing |
| [ ] | MC-08 | 8 | Shell, Tests, and Verification Loop |
| [ ] | MC-09 | 9 | Permission and Security |
| [ ] | MC-10 | 10 | Git Integration |
| [ ] | MC-11 | 11 | Session Persistence |
| [ ] | MC-12 | 12 | Quality, Evaluation, and Release |

### Status Legend

- `[ ]` Not teacher-verified
- `[x]` Passed all requirements and tests
- `PARTIAL` Some requirements passed, but work remains
- `FAIL` A required behavior or safety condition failed
- `BLOCKED` Verification could not run because the environment was unavailable

### Current Status

The project is currently in the planning and documentation stage. Implementation checkpoints have not yet been teacher-verified.

## Project Overview

The goal is to build a terminal-based coding agent that can use a local LLM to inspect a software project, search source code, propose safe changes, run verification commands, and explain its results.

The project uses Python as the main language and Ollama as the initial local LLM provider. The agent will be built in layers rather than hidden behind a pre-built agent framework.

## How It Works

```text
User request
    -> CLI
    -> Agent loop and context manager
    -> Local LLM
    -> Tool call or final answer
    -> Python validates permission
    -> File, search, patch, shell, or Git tool
    -> Tool result returns to the agent
    -> Final response or bounded verification loop
```

The LLM proposes an action. Python validates and executes that action. The LLM never receives direct access to the filesystem or shell.

## Learning Goals

- Build a practical Python CLI
- Understand agent loops and tool calling
- Practice HTTP, JSON, structured output, and async I/O
- Work with files, subprocesses, and Git
- Design context management and state persistence
- Implement patch review and human approval
- Learn permission boundaries and local-agent security
- Write unit, integration, and security tests
- Package and validate a cross-platform command-line application

## Target Scope

The target is a usable Level 3 local coding agent with:

- Interactive CLI
- Ollama provider abstraction
- Read-only project exploration
- Context management
- Patch-based file editing
- Permission-controlled shell execution
- Test and lint verification loops
- Git status and diff integration
- SQLite session persistence
- Windows-first cross-platform behavior

Multi-agent orchestration, browser automation, plugin marketplaces, autonomous execution, and production-grade sandboxing are outside the initial scope.

## Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Environment and packaging | `uv`, `pyproject.toml` |
| CLI | Typer |
| Terminal UI | Rich |
| HTTP | httpx |
| Validation | Pydantic v2 |
| Local model provider | Ollama |
| Tests | pytest |
| Lint and format | Ruff |
| Type checking | Pyright |
| Persistence | SQLite |

Additional libraries will be introduced only when a milestone requires them.

## Workflow

1. Read the next milestone in `Plan.md`.
2. Implement the work manually.
3. Run the milestone tests and record the evidence.
4. Ask the Teacher Agent to review the milestone.
5. Fix the findings if the result is not `PASS`.
6. When the result is `PASS`, the Teacher Agent updates only the matching status in this README.
7. Continue to the next major checkpoint.

## Repository Guides

- [`Plan.md`](Plan.md): complete curriculum, implementation tasks, tests, expected results, and acceptance criteria
- [`Agent.md`](Agent.md): Teacher Agent rules, review workflow, safety policy, and report format

## Example Commands

These commands become available progressively as milestones are completed:

```powershell
coder
coder ask "Find the cause of the failing test"
coder ask "Add validation and run the relevant tests"
coder status
coder resume <session-id>
```

## Definition of Done

The project is complete for the initial target when all `MC-00` through `MC-12` checkpoints are marked `[x]`, the full test suite passes, quality checks pass, and the final security and benchmark evaluations have evidence.
