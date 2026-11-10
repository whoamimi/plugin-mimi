---
name: react-native-like-mimi
description: Enforce functional-first, type-safe React Native and Expo development using TypeScript, Zod, hooks, composition, platform-aware components, and modular architecture. Use when writing, editing, or refactoring React Native TSX.
---

# React Native Modular Coding Style

## Core Principles

- Prefer functional components, hooks, and composition.
- Write small, pure, single-responsibility functions.
- Require strict TypeScript and typed component interfaces.
- Separate domain logic, presentation, and native side effects.
- Prefer immutable state and declarative rendering.
- Minimize dependencies, abstractions, and boilerplate.

## Type Safety & Schemas

- Enable TypeScript `strict: true`.
- Prefer `type` and `interface` for internal contracts.
- Use discriminated unions for categorical states.
- Use `as const` objects for reusable constants.
- Prefer `unknown` over `any`.
- Use generics and utility types where appropriate.

### Schema Selection

- **Zod:** API responses, forms, storage inputs, and runtime validation.
- **type / interface:** Component props and internal models.
- **Discriminated unions:** Navigation, loading, and feature states.
- **enum:** Only when interoperability requires it.
- Infer types from Zod rather than duplicating schemas.

## Functional Components

- Prefer named function components with explicit props.
- Use React Native primitives: View, Text, Pressable, etc.
- Prefer composition over class inheritance.
- Keep rendering pure and deterministic.
- Avoid unnecessary wrappers and deeply nested views.
- Extract shared UI components only when beneficial.

## Hooks & State

- Use typed custom `use*` hooks for reusable logic.
- Follow React's Rules of Hooks.
- Prefer local state before introducing global state.
- Use `useReducer` for complex state transitions.
- Use `useEffect` for external synchronization only.
- Clean up subscriptions, listeners, and async work.
- Avoid unnecessary memoization.

## Functional Patterns

- Prefer pure transformations and immutable updates.
- Use `map`, `filter`, `reduce`, and typed callbacks.
- Use generators and `yield` for lazy data processing.
- Use async generators when incremental streaming is useful.
- Prefer composition and higher-order functions over decorators.
- Keep business logic independent of React Native APIs.

## Native-Specific Conventions

- Use `StyleSheet.create` or an existing styling system.
- Use Flexbox and responsive layout primitives.
- Respect safe areas, accessibility, and touch targets.
- Use `FlatList` or `SectionList` for large collections.
- Prefer `Pressable` for interactive elements.
- Use `Platform.select` for small platform differences.
- Use `.ios.tsx` / `.android.tsx` for larger differences.
- Prefer Expo-compatible APIs when the project uses Expo.
- Avoid browser-only DOM APIs in native components.

## Navigation & Data

- Use typed navigation parameters and route contracts.
- Keep navigation concerns outside pure business logic.
- Validate external and persisted data with Zod.
- Encapsulate storage, networking, and device APIs.
- Avoid storing secrets in unencrypted device storage.
- Handle offline, loading, and error states explicitly.

## Performance & Lifecycle

- Avoid expensive computations during render.
- Prefer virtualized lists for large datasets.
- Avoid unnecessary rerenders and duplicated state.
- Respect app foreground/background lifecycle.
- Clean up listeners and subscriptions.
- Optimize only after identifying actual bottlenecks.

## Testing & Quality

- Use ESLint, TypeScript, and consistent formatting.
- Test pure functions independently.
- Use React Native Testing Library for UI behavior.
- Validate iOS and Android platform differences.
- Test accessibility and touch interactions.

## Refactoring Rules

1. Preserve existing behavior and public interfaces.
2. Introduce strict types and appropriate Zod schemas.
3. Extract reusable pure business logic.
4. Introduce hooks for reusable stateful behavior.
5. Separate platform-specific code where justified.
6. Avoid unnecessary wrappers and dependencies.
7. Add or update focused tests.

## Output Expectations

- Produce concise, type-safe, production-quality React Native.
- Prefer functional core and imperative shell architecture.
- Favor cross-platform reuse without forcing identical UI.
- Keep components modular, accessible, and responsive.
- Avoid overengineering and redundant abstractions.

## Example Directory Structure

src/
├── components/ # Reusable native UI
├── features/ # Feature-specific modules
├── hooks/ # Shared custom hooks
├── schemas/ # Zod schemas and contracts
├── lib/ # Pure functions and API clients
├── services/ # Device and platform integrations
└── app/ # Navigation and application setup
