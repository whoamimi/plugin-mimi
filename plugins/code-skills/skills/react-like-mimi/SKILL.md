---
name: react-like-mimi
description: Enforce functional-first, type-safe React Web development using TypeScript, Zod, hooks, composition, and modular architecture. Use when writing, editing, or refactoring React and TSX.
---

# React Web Modular Coding Style

## Core Principles

- Prefer functional components and composition over class components.
- Write small, pure, single-responsibility functions.
- Require TypeScript strict mode and explicit public interface types.
- Prefer immutable state and declarative rendering.
- Separate business logic, UI presentation, and side effects.
- Avoid unnecessary abstractions, dependencies, and boilerplate.

## Type Safety & Schemas

- Use TypeScript with `strict: true`.
- Prefer `type` for unions and data shapes; `interface` for extensible contracts.
- Use discriminated unions for categorical state.
- Use `as const` for immutable categorical constants.
- Prefer `unknown` over `any` for untrusted values.
- Use generics and utility types where justified.
- Avoid unsafe type assertions and non-null assertions.

### Schema Selection

- **Zod:** External API contracts, forms, configuration, and runtime validation.
- **type / interface:** Internal models, component props, and contracts.
- **Discriminated unions:** Finite states and variant-based behavior.
- **enum:** Only when interoperability or an existing API requires it.
- Infer TypeScript types from Zod schemas where appropriate.

## Functional Components

- Prefer named function declarations for components.
- Define explicit, readonly props.
- Keep rendering deterministic and free of side effects.
- Prefer composition and children over inheritance.
- Extract reusable logic only when duplication justifies it.
- Avoid unnecessary `React.FC` and wrapper components.

## Hooks & State

- Use custom `use*` hooks for reusable stateful logic.
- Follow the Rules of Hooks unconditionally.
- Prefer derived state over duplicated state.
- Use `useReducer` for complex state transitions.
- Use `useEffect` only for external synchronization.
- Avoid unnecessary `useMemo` and `useCallback`.
- Keep event handlers explicit and properly typed.

## Functional Patterns

- Prefer `map`, `filter`, `reduce`, and pure transformations.
- Use `function*` and `yield` for lazy iteration when beneficial.
- Use async generators for supported streaming workflows.
- Prefer typed callbacks for optional extension points.
- Use higher-order functions for genuinely reusable behavior.
- Avoid decorator patterns for React components and hooks.

## Web-Specific Conventions

- Prefer semantic HTML and accessible native controls.
- Use typed DOM events and keyboard interactions.
- Use CSS modules, scoped styles, or existing design systems.
- Separate API clients from components.
- Clean up listeners, subscriptions, and requests.
- Respect existing routing and server/client boundaries.

## Testing & Quality

- Use ESLint, TypeScript, and consistent formatting.
- Test pure functions independently.
- Use React Testing Library for component behavior.
- Verify keyboard accessibility and interaction states.
- Preserve public interfaces during refactoring.

## Refactoring Rules

1. Preserve existing behavior and component contracts.
2. Introduce strict types and appropriate Zod schemas.
3. Extract repeated logic into pure functions.
4. Introduce hooks only for reusable React logic.
5. Prefer composition over additional wrappers.
6. Avoid redundant state, effects, and memoization.
7. Add or update focused tests.

## Output Expectations

- Produce concise, type-safe, accessible React and TSX.
- Prefer functional core and imperative shell architecture.
- Keep components presentational where practical.
- Minimize boilerplate, dependencies, and coupling.
- Explain architectural decisions only when necessary.

## Example Directory Structure

src/
├── components/ # Reusable UI components
├── features/ # Feature-specific modules
├── hooks/ # Shared React hooks
├── schemas/ # Zod contracts and types
├── lib/ # Pure utilities and API clients
└── app/ # Routes and application setup
