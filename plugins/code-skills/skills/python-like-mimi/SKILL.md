---
name: python-like-mimi
description: Enforce functional-first, type-safe Python with Pydantic, dataclasses, enums, decorators, hooks, and lightweight modular architecture. Use when writing, editing, or refactoring Python.
---

# Python Modular Coding Style

## Core Principles

- Prefer functional programming and composition over inheritance.
- Write small, pure, single-responsibility functions.
- Require explicit type annotations for parameters and returns.
- Follow PEP 8 and modern Python conventions.
- Minimize mutable state, dependencies, and abstractions.
- Separate business logic from I/O and side effects.

## Type Safety & Schemas

- Use Python 3.11+ typing conventions.
- Prefer built-in generics: `list[str]`, `dict[str, int]`.
- Use `X | None` instead of `Optional[X]`.
- Use `Protocol`, `TypeAlias`, and generics where justified.
- Use `Enum` or `StrEnum` for fixed categorical values.
- Use `Literal` for small, context-specific value constraints.
- Avoid `Any` unless unavoidable.

### Schema Selection

- **Pydantic v2 BaseModel:** API contracts, external data,
  configuration, serialization, and runtime validation.
- **dataclasses:** Internal typed data structures and
  lightweight domain models without runtime validation.
- **Enum / StrEnum:** Reusable categorical constants.
- **TypedDict:** Lightweight typed dictionary interfaces.

## Design Patterns

- **Functions:** Keep domain logic independently testable.
- **Decorators:** Reuse logging, retries, caching, and validation.
- **Hooks:** Prefer typed callbacks for extensibility.
- **Dependency Injection:** Pass dependencies explicitly.
- **Composition:** Prefer small functions over class hierarchies.
- **Modules:** Organize by feature and responsibility.

## Conventions

- Prefer `@dataclass(frozen=True, slots=True)` for immutable models.
- Use Pydantic `Field` and validators for external constraints.
- Prefer `pathlib`, `collections.abc`, and standard-library tools.
- Use `async`/`await` only for asynchronous I/O.
- Avoid global mutable state and hidden side effects.
- Raise specific exceptions; never silently swallow errors.
- Add concise docstrings for non-obvious behavior.
  -Usage: Pydantic validates inputs and outputs at system boundaries; frozen dataclasses represent internal domain state; enums encode finite states; typed functions implement business logic; decorators and callbacks provide reusable extension points.

## Refactoring Rules

1. Preserve existing behavior and public interfaces.
2. Introduce explicit types and appropriate schemas.
3. Extract repeated logic into reusable functions.
4. Introduce decorators or hooks only when justified.
5. Keep modules loosely coupled and independently testable.
6. Avoid unnecessary classes, wrappers, and dependencies.
7. Add or update focused tests for changed behavior.

## Output Expectations

- Produce concise, type-safe, production-quality Python.
- Prefer functional core and imperative shell architecture.
- Use Pydantic only where runtime validation is beneficial.
- Avoid overengineering and redundant abstractions.
- Explain architectural decisions only when necessary.

## Example Directory Structure

```
inventory-mcp/
├── pyproject.toml
└── src/
    └── inventory/
        ├── __init__.py
        ├── schemas.py       # Pydantic, dataclasses, enums
        ├── core.py          # Pure functions and generators
        └── server.py        # MCP decorators and lifecycle hooks
```
