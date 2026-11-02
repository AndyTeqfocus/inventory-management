---
name: vue-component-analysis
description: Analyze a Vue 3 component's structure and produce a prioritized report of performance and code-reuse optimizations, measured against this repo's Composition API conventions. Use when asked to analyze, audit, review or optimize a .vue file, or when asked "what's wrong with this component".
---

# Vue Component Analysis

Read-only analysis. This skill produces a report; it does not edit files.
If the user wants the fixes applied afterwards, delegate the `.vue` edits to the
`vue-expert` subagent (repo rule) and hand it the report.

## Inputs

- One or more `.vue` paths. If none is given, ask which, or analyze
  `client/src/views/*.vue` when the user says "all views".
- Always read the target file in full, plus the reference pattern files below,
  before writing anything. Also grep `client/src/utils/` and `client/src/locales/`
  for helpers and keys that already exist before proposing new ones.

## Reference files (the standard this repo expects)

| File | What it shows |
|---|---|
| `client/src/views/Orders.vue` | Canonical view: `setup()`, `api` client, `useFilters`, `useI18n`, `watch` on filters |
| `client/src/api.js` | The only place HTTP calls belong |
| `client/src/composables/useFilters.js` | Shared filter state and `getCurrentFilters()` |
| `client/src/composables/useI18n.js` | `t()`, `currentLocale`, `currentCurrency`, name translators |
| `client/src/App.vue` | Global styles: `.card`, `.stat-card`, `.badge`, `.page-header`, tables, `:root` tokens |
| `client/src/utils/currency.js` | `formatCurrency` / `formatCurrencyWithDecimals`, the money formatters Dashboard and Spending use |
| `client/src/locales/en.js` | Existing keys to reuse before inventing new ones: `common.*`, `months.*`, `status.*`, `nav.*` |
| `client/CLAUDE.md` | The written conventions |

## Checklist

Work through every item. Record a finding only when the file actually violates it.

### A. Architecture (must match the rest of the app)
1. **API style**: `export default { name, setup() }` with Composition API. Options API
   (`data()`, `methods:`, `mounted()`) is a finding.
2. **Data access**: all HTTP goes through `api` from `client/src/api.js`. A direct
   `axios.get(...)` or a hardcoded `http://localhost:8001` URL is a finding. If the
   endpoint has no `api` method yet, say which one to add.
3. **Filters**: views that show filterable data must use `useFilters()`, pass
   `getCurrentFilters()` to the API, and `watch` the four filter refs to reload.
   If the backend endpoint ignores those query params, record it as a view finding
   (wire the view now) and name the server gap in the refactor order.
4. **i18n**: every user-visible string goes through `t('...')`; currency uses
   `currentCurrency`; dates use `currentLocale`. Hardcoded English is a finding.
   Also check `nav.*` keys exist in both `locales/en.js` and `locales/ja.js`.
5. **Logging**: no `console.log` left in production paths. `console.error` inside
   a `catch` is acceptable.

### B. Reactivity and performance
6. **Derived data in `computed`**, never recomputed in methods called from the
   template. A method invoked per row that loops over the whole dataset (for
   example a max computed inside a bar-height helper) is an O(n²) render.
7. **`v-for` keys**: unique domain keys (`sku`, `id`, `month`, `quarter`), never
   the array index.
8. **Date handling**: validate any date or month input before indexing or
   formatting it: `isNaN(new Date(x).getTime())` for dates, a shape check such as
   `/^\d{4}-\d{2}$/` for `YYYY-MM` strings.
9. **Loading / error states**: `loading` and `error` refs, try/catch/finally, and
   both states rendered in the template.
10. **Watchers**: no watcher that re-fetches on every keystroke without debounce;
    no watcher duplicating what a `computed` would do.
11. **Large templates**: a template over ~100 lines or logic over ~150 lines is a
    candidate for extracting a child component.

### C. Code reuse
12. **Formatting helpers**: hand-rolled number/currency/date formatting should use
    `toLocaleString` or an existing helper; look for the same helper duplicated in
    other views and suggest a composable.
13. **Styles**: scoped CSS that re-declares `.card`, `.stat-card`, `.badge`, table
    or loading/error styles already in `App.vue` is dead weight. Only keep
    component-specific rules.
14. **Shared composables**: logic that exists in another view (status class maps,
    status filtering, growth calculations) belongs in `composables/`.

## Report format

Write the report in this shape and nothing else:

```
# Component analysis: <path>

**Verdict**: one sentence (fine / needs work / rewrite recommended).

## Findings (highest impact first)
| # | Area | Finding | Where | Fix |
|---|------|---------|-------|-----|
| 1 | Architecture | ... | line N / template / style | ... |

## Suggested refactor order
1. ...  (what to do first and why; keep to 3–6 steps)

## Not an issue
- Things that look suspicious but are fine in this codebase, with the reason.
```

Rules for the report:
- Cite line numbers or template/section names so the fix can be located.
- Rank by user impact: broken behavior (filters ignored, wrong language) first,
  then performance, then reuse and style.
- Keep each finding to one line in the table; put nuance in the refactor order.
- Do not propose changing routes, `api.js` signatures, composable APIs or locale
  key names; the fix must fit the existing patterns.

## Example trigger prompts

- "Analyze client/src/views/Reports.vue"
- "Audit the Spending view for performance problems"
- "What should be refactored in Dashboard.vue?"
