# Component analysis: client/src/views/Reports.vue

Generated with the `vue-component-analysis` skill (workshop Step 12 test run).

**Verdict**: Rewrite recommended. The view is Options API, bypasses `api.js`, ignores the global filters and i18n entirely, and recomputes derived data per render.

## Findings (highest impact first)
| # | Area | Finding | Where | Fix |
|---|------|---------|-------|-----|
| 1 | Architecture | Global filters ignored: no `useFilters()`, no `watch` on the filter refs | script `mounted`/`loadData` | Wire `useFilters()` + `watch(...)` as in Orders.vue; pass `getCurrentFilters()` to the API (server `/api/reports/*` ignores params today) |
| 2 | Architecture | Zero i18n: headings, table headers, stat labels, loading text, month names, `'N/A'` all hardcoded English | template throughout; script `formatMonth`, `getGrowthRate` | Add `reports.*` keys to en.js and ja.js; reuse `common.loading`, `months.*` |
| 3 | Architecture | Currency hardcoded as `$`; `currentCurrency` unused | template money cells; script `getChangeValue` | Use `formatCurrencyWithDecimals(v, currentCurrency.value, 2)` from `utils/currency.js` |
| 4 | Architecture | Direct `axios.get('http://localhost:8001/...')` instead of the `api` client | script `loadData` | Add `api.getQuarterlyReports(filters)` and `api.getMonthlyTrends(filters)` |
| 5 | Architecture | Options API (`data()`, `mounted()`, `methods:`), the only view not on `setup()` | whole script | Port to `export default { name, setup() }` |
| 6 | Architecture | 13 `console.log` calls, three inside per-row helpers; `catch` logs with `console.log` | script | Delete all; keep one `console.error` in the catch |
| 7 | Performance | `getBarHeight` rescans all of `monthlyData` for the max on every bar (O(n²) per render) | script `getBarHeight` | `maxRevenue` computed |
| 8 | Performance | Summary stats stored as state and recomputed imperatively; change/growth helpers re-run per cell | script `calculateSummaryStats`, template MoM table | Make the four stats `computed`; add a `monthlyRows` computed with change/growth precomputed |
| 9 | Performance | `v-for` keyed by array index in all three lists | template | `:key="q.quarter"`, `:key="month.month"` |
| 10 | Performance | `formatMonth` splits `YYYY-MM` with no validation | script `formatMonth` | Guard the shape; fall back to the raw value |
| 11 | Performance | Two sequential awaits for independent endpoints | script `loadData` | `Promise.all` |
| 12 | Performance | Template ~125 lines, script ~190 lines | file | Extract `MonthlyRevenueChart.vue` (optional) |
| 13 | Reuse | Hand-rolled 30-line `formatNumber` | script | Replace with `formatCurrencyWithDecimals`; delete |
| 14 | Reuse | Growth/change logic and month-label map duplicate Spending.vue | script | Hoist to a shared composable (optional) |
| 15 | Style | Scoped CSS re-declares `.card`, tables, `.stats-grid`, `.stat-*`, `.badge*`, `.loading`, `.error` already global in App.vue, with drifted values | style | Delete those blocks; keep only chart and change-colour rules |
| 16 | Style | `.bar-label` sets `margin-top` twice | style | Keep one |

## Suggested refactor order
1. Port to `setup()` with `api` + `useFilters` + `watch` (1, 4, 5, 11). Add the two `api.js` methods first.
2. i18n and currency pass (2, 3, 13): new `reports.*` keys only, reuse `months.*` and `common.loading`.
3. Move derived data to `computed` (7, 8, 9, 10); delete every `console.log` (6).
4. Strip scoped CSS to chart and change-colour rules (15, 16).
5. Optional: extract the chart component and hoist growth helpers (12, 14).

## Not an issue
- `nav.reports` exists in both locale files; the sidebar label and top-bar title are localised.
- Loading and error states exist with try/catch/finally.
- `getFulfillmentClass` returns real global badge classes; they work once scoped overrides are removed.
- Chart CSS (`.bar-*`, `.chart-container`) and `.positive-change`/`.negative-change` are component-specific and should stay scoped.
