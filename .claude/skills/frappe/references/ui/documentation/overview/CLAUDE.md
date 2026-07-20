# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**frappe-ui** is a Vue 3 component library and utilities package for building Frappe-based web applications. Used in production by Frappe Cloud, Gameplan, Helpdesk, Insights, Drive, and Builder.

## Common Commands

```bash
# Development
yarn dev              # Start Vite dev server
yarn test             # Run tests with Vitest
yarn type-check       # TypeScript type checking

# Documentation
yarn docs:dev         # Start docs dev server
yarn docs:build       # Build documentation

# Release
yarn bump-and-release # Run tests, pull, bump patch version, push with tags
```

## Tech Stack

- **Framework**: Vue 3 with Composition API (`<script setup>`)
- **Language**: TypeScript
- **Build**: Vite
- **Styling**: TailwindCSS v3 with semantic color system
- **UI Primitives**: Reka UI (migrating from Headless UI)
- **Rich Text**: TipTap v3 (ProseMirror)
- **Testing**: Vitest with MSW for mocking

## Architecture

### Project Structure

```
src/
├── components/       # Vue components (Button, Dialog, etc.)
├── data-fetching/    # v2 composables (useDoc, useList, useCall) - TypeScript-first, Frappe API v2
├── resources/        # v1 utilities (createResource, etc.) - Options API compatible, Frappe API v1
├── composables/      # Reusable Vue composables
├── directives/       # Custom Vue directives
├── utils/            # Utility functions
vite/                 # Vite plugins for Frappe integration
tailwind/             # Tailwind preset and theme plugin
frappe/               # High-level Frappe-specific modules
icons/                # Custom SVG icon components
docs/                 # VitePress documentation
```

### Component Structure

Each component follows this directory pattern:
```
src/components/ComponentName/
├── ComponentName.vue   # Main component
├── types.ts            # TypeScript types (required)
├── index.ts            # Public exports
└── stories/            # Visual examples (Sizes.vue, Variants.vue, etc.)
```

### Type Naming Conventions (Critical)

These naming patterns are mandatory - they drive documentation generation:
- Props: `ComponentNameProps`
- Emits: `ComponentNameEmits`
- Slots: `ComponentNameSlots`
- Exposed Methods: `ComponentNameExposed`
- Union Types: `ComponentNameSize`, `ComponentNameVariant`, etc.

All props, events, and slots require JSDoc descriptions.

### Data Fetching

**v2 (Current)** - `src/data-fetching/`: TypeScript-first composables for Vue 3 + Frappe API v2
- `useDoc` - Single document operations
- `useList` - Document list operations
- `useCall` - Generic API calls

**v1 (Legacy)** - `src/resources/`: Vue 2 compatible, Frappe API v1
- `createResource`, `createListResource`, `createDocumentResource`

Use v2 for new projects with Vue 3. v1 remains stable for existing projects.

## Key Conventions

### Icons
- Use Lucide icons (auto-imported): `<LucideCheck class="size-4" />`
- FeatherIcon is deprecated - do not use in new code

### Styling
Use semantic colors instead of hardcoded values:
- Backgrounds: `bg-surface-{white|gray-1..9|black}`
- Text: `text-ink-{white|gray-1..9|black}`
- Borders: `border-outline-{white|gray-1..5|black}`
- Use `size-{n}` instead of `w-{n} h-{n}` for square elements

### Component Design
- Prefer `v-model` for two-way binding
- Name events by behavior (`change`, `open`, `close`) not interaction (`toggle`, `click`)
- Split focused components rather than overloading with props
- Prefer primitive prop types over complex objects

### What to Avoid
- Don't use `<style scoped>` unless Tailwind can't express the styling
- Don't add unnecessary comments - only explain "why" not "what"
