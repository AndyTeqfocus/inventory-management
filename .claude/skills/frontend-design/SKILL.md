---
name: frontend-design
description: Redesign a Vue 3 application's UI into a modern SaaS-style interface with a dark vertical sidebar on the left, a light content area, consistent spacing tokens, and polished card layouts. Use when asked to restyle, modernize, or "make it look like a SaaS product", or when adding a sidebar/app-shell layout to a Vue app.
---

# Frontend Design — SaaS App Shell for Vue 3

Turn a top-nav Vue 3 app into a sidebar-based SaaS interface without changing behavior, routes, API calls, or i18n keys.

## Visual direction (locked)

- **Shell**: dark sidebar (`--sidebar-bg: #0f172a`), light content (`--content-bg: #f8fafc`), white cards.
- **Accent**: blue `#3b82f6` for active nav, focus rings, primary buttons. Status colors stay green/blue/yellow/red.
- **Type**: system sans (`-apple-system, Inter, Segoe UI, sans-serif`), 14px base, 600 for headings. No emojis in UI.
- **Spacing scale**: 4 / 8 / 12 / 16 / 24 / 32 px as `--space-1..6`. Cards use 20px padding, 12px radius, 1px `#e2e8f0` border, no heavy shadows.
- **Sidebar**: fixed, 240px wide, full height. Logo + subtitle on top, one row per route with a 20px inline-SVG icon and label, language switcher and profile menu pinned at the bottom. Active row: `rgba(59,130,246,.15)` background, white text, 3px blue left rail.
- **Top bar**: page title (from the route) on the left, filter bar on the right, 64px tall, white, bottom hairline.
- **Content**: `margin-left: 240px`, max-width 1400px, 32px padding, CSS Grid for card rows.

## Scope rules

1. **Shell first, views second.** Edit `App.vue` (layout + global tokens) and `FilterBar.vue`. Add shared classes (`.card`, `.page-header`, `.kpi-grid`, `.section-title`) in global CSS so views inherit the look. Only touch individual views when explicitly asked.
2. **Never change** routes, `api.js`, composables, locale keys, or data shapes. Nav labels keep using `t('nav.*')`.
3. **Preserve** every existing component (LanguageSwitcher, ProfileMenu, modals, FilterBar) by moving it, not rewriting it.
4. **Responsive**: below 1024px the sidebar collapses to 64px icons-only; below 768px it becomes a top drawer. Content margin follows.
5. **Accessibility**: nav is a `<nav aria-label="Main">`, active link has `aria-current="page"`, icons are `aria-hidden`, focus rings visible.

## Process

1. Read `App.vue`, `FilterBar.vue`, one representative view (Dashboard), and the locale file to collect nav labels and existing CSS variables.
2. Draft the token block (`:root` variables) and the shell markup. Keep the old class names where views depend on them.
3. Implement in this order: tokens → sidebar → top bar + filter bar → content wrapper → shared card classes → responsive rules.
4. Verify in the browser at http://localhost:3000 on every route: sidebar highlights the current route, filters still change data, modals still open, language switch still works, no console errors.
5. Summarize what changed and what views may still need per-page polish.

## Delegation

Per project rules, `.vue` edits go through the `vue-expert` subagent. Hand it this skill's token block and scope rules verbatim.

## Anti-patterns

- Introducing a CSS framework or component library.
- Replacing inline SVG charts or CSS Grid layouts.
- Hardcoding English strings that have `t()` keys.
- Box-shadow heavy "card soup"; prefer hairline borders and whitespace.
