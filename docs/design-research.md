# JobMatch AI — Design Research: Visual Direction, Tokens, and Component Patterns

**Date:** 2026-11-14 · **Scope:** student-side internship eligibility & fit analysis (React 18 + TS + Vite, plain CSS, lucide-react)
**Stack constraint honoured:** zero new runtime dependencies; fonts via Google Fonts `<link>` only; native `<dialog>` instead of a modal library.

## 0. Verdict

**Adopt "Instrument / Swiss-editorial":** an International-Typographic-Style grid, paper-and-ink surfaces, one structural accent, monospace for all machine facts, and state encoded by icon + label + colour — never colour alone.

Reject glassmorphism, neumorphism, and literal neo-brutalism as *systems*. Borrow from them narrowly:

| Direction | Verdict | Take | Leave |
|---|---|---|---|
| Swiss / editorial | Core system | 12-col grid, flush-left, 1px rules, tabular data, asymmetric composition | Museum-style giant whitespace |
| Neo-brutalism | Accent only | Flat fills, hard 2px section rules, zero-blur borders, confident display type | 4px offset black shadows on every element, rotations, neon blocks |
| Neumorphism | Reject | Nothing structural | Inset/embossed controls — fails non-text contrast and clickability |
| Glassmorphism | Reject except transient overlays | Nothing on content surfaces | Blur behind text, translucent cards |
| Bento grid | Reject for app, allow on marketing | Unequal tile rhythm for a "how it works" strip | Bento as dashboard layout |
| Tactile | Texture only | 2–3% paper grain, 1px rules, letterpress-like weight | Soft embossing, depth-faking gradients |

Trust in a decision-support product is produced by predictability and legibility, not novelty. Soft-green SaaS cards, glass, and embossing spend contrast and vertical space on decoration — the two resources a rules engine cannot spare. The redesign should read as an **instrument panel / audit exhibit**, not a wellness app.

## 1. Landscape (2025–26)

- **Neo-brutalism** — high contrast, blocky layouts, bold colours, thick borders, "unpolished" elements, stark single-colour offset shadows; NN/g warns "without balance, it can overwhelm users and hinder accessibility" (NN/g, 2025-04-11). Its canonical examples (Gumroad, Figma's 2023 refresh) are *marketing* surfaces with low information density. Offset shadows + 3px borders cost 6–12px per element — a 20–30% density tax at 36px table rows.
- **Neumorphism** — light-grey-on-white controls are "barely possible to see" ("ghost UI"), plus unlabeled icons and ambiguous clickability; fixes require 4.5:1 text and 3:1 for borders/icons (Axess Lab, 2020-04-09). WCAG 1.4.11 (3:1 non-text) is what the entire style erases. Closed case for WCAG 2.2 AA.
- **Glassmorphism** — returned via Apple "Liquid Glass" (WWDC 2025); even sympathetic 2025 pieces concede: do not use for "forms with a lot of text", "data-heavy tables", or "interfaces requiring maximum readability" (Medium, 2025-12-06). Allowable only for a modal backdrop over a *solid* surface, with `backdrop-filter` disabled under `prefers-reduced-transparency`.
- **Swiss/editorial** — mathematical grid, sans-serif flush-left/ragged-right, objective imagery, asymmetric composition; "stripping ornament lets information-heavy design be read and studied" (PRINT, 2020-01-31). This is literally a description of an audit tool.
- **Bento grids** dominate marketing/portfolio pages; in an app, unequal tiles imply a hierarchy the data does not have, re-adding padding a table would not need.
- **Tactile (2026)** — soft shadows and gradients "almost touchable". Take the *paper* metaphor, not the *foam* metaphor: grain + rules + weight, not embossing.

## 2. Why "Instrument" fits the product

| Requirement | Swiss-editorial answer | Why alternatives fail |
|---|---|---|
| Trust | Stable grid, consistent 1px rules, no decorative variance | Glass/neumorphism alter perceived contrast per scroll |
| Legibility at density | 14px base, 1.55 body, 13px secondary, 32–36px rows | Bento/brutalism add 12–24px padding per container |
| State signalling | Icon + text label + tint + 3px semantic left rule | Colour-only chips fail WCAG 1.4.1 and red/green CVD |
| Long-form evidence | 13px/1.55 on 60–72ch measure, serif for quoted source text | Glass over text destroys contrast |
| Tables/checklists | Tabular numerals, right-aligned quantities, 1px row rules | Cards cannot align columns |
| WCAG 2.2 AA | 4.5:1 text, 3:1 controls, 24×24 targets, visible focus | Neumorphism fails 1.4.11 by design |

WCAG 2.2 obligations designed against explicitly: 1.4.3 (4.5:1 text), 1.4.11 (3:1 non-text), 2.4.11 (focus not obscured by sticky headers → `scroll-padding-top`), 2.5.7 (drag alternatives — a drag-only résumé dropzone is non-conformant), 2.5.8 (24×24 targets), 2.4.13 (AAA focus indicator ≥2px/3:1, adopted anyway).

## 3. Design tokens (implemented in `src/styles/tokens.css`)

### Typefaces — IBM Plex superfamily (OFL, Google Fonts)
One superfamily, three roles: **Plex Sans** (UI + headings), **Plex Mono** (every machine fact: scores, rule IDs, dates, file sizes, counts), **Plex Serif** (quoted evidence/report prose). Designed for IBM's technical documentation as a coherent sans/mono/serif system. Avoids the "Inter default" that is the first tell of AI-generated UI.

### Colour — paper/ink + one accent + five semantic states
All ratios computed with the WCAG relative-luminance formula. Body text ≥4.5:1, controls ≥3:1.

```
Surfaces: --paper #F8F7F3 · --surface #FFFFFF · --surface-2 #EFEDE6 · --surface-3 #E4E1D7
Ink:      --ink #111315 (17.37:1) · --ink-2 #3A4048 (9.76:1) · --ink-3 #5C636E (5.65:1)
Rules:    --rule #D6D3CA (decorative) · --rule-strong #111315 (2px section rules) · --border-control #8A8F98 (3.25:1)
Accent:   --accent #1F4FD8 (6.63:1) · --accent-hover #1A44BB · --accent-wash #E9EEFC
Pass:     --pass-fg #0B6B3F / --pass-bg #E7F3EC / --pass-bd #A9D3BB (5.78:1)
Warn:     --warn-fg #8A4B00 / --warn-bg #FBF0DA / --warn-bd #E8C88E (6.02:1)
Fail:     --fail-fg #B42318 / --fail-bg #FDE8E6 / --fail-bd #EFB4AE (5.59:1)
Info:     --info-fg #1A4FA0 / --info-bg #E7EFFB / --info-bd #AEC4E8 (6.79:1)
Unknown:  --unknown-fg #4A5160 / --unknown-bg #ECEBE6 / --unknown-bd #C3C2BA (6.67:1)
```

Rules of use: semantic fills are never the sole carrier of meaning — every state also ships a lucide icon and a word ("Pass", "Needs input", "Unknown"). "Unknown" is a first-class state with its own neutral colour, not an empty cell.

### Type scale, space, radius, border, shadow
- 14px default UI, 13px secondary, 12px mono labels; 36/22/16/… headings; `tabular-nums` mandatory in every table, score, count, duration, date.
- Space: 4/8/12/16/20/24/32/40/48/64.
- Radius: 2px (chips/inputs/code), 4px (buttons/cards/tables), 6px (dialogs only). No 8/12/16px tier — the single most reliable "generic SaaS" tell.
- Cards get a 1px border and no shadow. Shadows exist only for `--shadow-2` on dialogs/sheets/popovers. Hard offset shadows (6px 6px 0 ink) are reserved for the hero specimen card and the analyze CTA — the neo-brutalist accent.
- Motion: 90/140/200ms, `cubic-bezier(.2,0,0,1)`; animate opacity + 2px translate only; no height/width/scale; no load orchestration; `prefers-reduced-motion` fully respected.

### Migration performed
Deleted the `@import` of DM Sans/Manrope (render-blocking), deleted `--green/--green-dark`, mapped old values to new tokens, removed all `border-radius ≥ 8px`, and set `scroll-padding-top: 80px` so the sticky header never obscures focus.

## 4. Component patterns (implemented)

- **Verdict block** (not a bare number): band word first, number second, provenance third — "78 /100 fit", 5-segment meter, "14 of 16 criteria resolved · 2 need your input".
- **Eligibility ledger**: 36px rows, 1px bottom rules, tri-state icon + word + rule ID in mono + source link; disclosure reveals exact rule text.
- **Evidence / skill matrix**: columns Requirement · Evidence · Source · Status; expand a row to reveal the quoted résumé line in Plex Serif behind a 2px left rule.
- **Alert / warning card**: 3px left rule, square 2px radius, icon + title + one-sentence body + underlined action. No coloured bubble.
- **Upload dropzone**: drag is an enhancement; click-to-browse and paste-text are primary (WCAG 2.5.7). File metadata in mono. Determinate progress, inline error via `aria-describedby`.
- **Filter tabs**: underline tabs with 2px active rule; counts in mono; `role="tab"` + `aria-selected`; roving tabindex + arrow keys.
- **Comparison table**: sticky `thead`, sticky first column, hover row tint, no zebra (zebra fights hover/focus), unknown rendered as `—` with legend.
- **Modal / evidence sheet**: native `<dialog>` + `showModal()` — built-in focus trap, `Esc`, `::backdrop`; no dependency, no re-implementation bugs. Right-side sheet 480px for evidence; centred 560px for destructive confirmation. The only place `--shadow-2` appears.
- **Empty state**: no blob illustration. Three ghost rows at 36px, one sentence naming the next action, one primary button.
- **Unknown-state callout**: neutral `--unknown-*` block — "We cannot verify this from your profile. It will not be counted for or against you." Explicitly excluding unknowns from the numerator is what makes the score auditable.

## 5. Anti-patterns avoided

1. Purple→blue gradient hero and gradient CTA fills.
2. Inter/system font with no typographic decision; uniform 16px radius on every element.
3. Uniform card grid for heterogeneous data (20 criteria do not deserve 20 cards).
4. Fake precision: "87.3% match" with no n-of-m, no rule IDs, no source links.
5. Colour-only status (green dot vs red dot) — fails 1.4.1 and red/green CVD.
6. Emoji or sparkle icons as state.
7. Glass or blur behind evidence text; translucent sticky headers over tables.
8. Soft shadow on every card.
9. Oversized marketing hero above a working tool — the first viewport contains the upload surface.
10. Load animations and staggered reveals on a page whose job is to show data immediately.
11. Centred numeric columns and proportional figures in tables.
12. Muted grey below 4.5:1 used for "secondary" text.
13. Icon-only navigation without labels.
14. Drag-only upload (non-conformant with WCAG 2.5.7).

## 6. Reference products & what to borrow

| Source | Why exemplary | Borrow specifically |
|---|---|---|
| GOV.UK Design System (v6.6.0) | Highest-stakes public service on the web; functional colour naming, 4.5:1 mandate, focus yellow `#ffdd00` with black text, plain-language errors | Functional token names, "one thing per page" rule for the eligibility wizard, error-summary pattern |
| Vercel Geist (typography 2025-11-25) | Type system split into Label/Copy/Mono with explicit tabular variants | 14px default, 13px secondary, 12px mono labels; separate UI vs prose line-heights; mono+tabular for numbers |
| IBM Carbon data table (2026-09-30) | Five documented row densities (24/32/40/48/64px), expandable rows, toolbar, "give tables the most width" | 32px compact / 40px default rows, expandable row detail, table toolbar |
| Linear | Density without clutter: near-black text on off-white, 1px borders, almost no shadow, keyboard-first | Border-only cards, restrained hover tints, command palette for jumping to a criterion |
| Stripe | Best-in-class documentation typography and code/evidence blocks | Type hierarchy and inline code treatment — not the gradient marketing hero |

## 7. Sources

1. NN/g — Neobrutalism: Definition and Best Practices (2025-04-11) — definition, examples, usability/contrast warnings.
2. Axess Lab — Neumorphism, the accessible and inclusive way (2020-04-09) — contrast failures, "ghost UI", 4.5:1 / 3:1.
3. UX Collective — Let's talk Neumorphism and Accessibility (2020-02-11).
4. Medium/xurxe — For a more accessible Neumorphism (2020-01-31) — origin (Plyuto), coiner's retraction.
5. Curb Cuts — Apple's Liquid Glass won't make the sky fall (2025-06-10).
6. TidBITS — Liquid Glass Prioritizes Content Over Tools (2025-10-06) — "nearly illegible" translucency.
7. Medium — Glassmorphism in 2025 (2025-12-06) — where glass must not be used.
8. Figma — Top Web Design Trends for 2026 (2026-06-11) — trend inventory.
9. Mockuuups — Best Bento Grid Examples 2026 (2024-02-22, 2026 ed.).
10. PRINT — Swiss Style: Principles, Typefaces & Designers (2020-01-31).
11. The Graphic Design School — Swiss Style (2026-01-01).
12. 925Studios — AI Slop Web Design Guide (2026).
13. Impeccable — Slop (2026-01-30).
14. W3C — WCAG 2.2 (Rec. 2023-10-05, upd. 2024-12-12).
15. AccessibleMetrics — WCAG 2.2: 9 New Criteria Explained (2026-09-07).
16. GOV.UK Design System — Colour (retrieved 2026-11-14).
17. Vercel Geist — Typography (2025-11-25) and Colors.
18. IBM Carbon — Data table usage (2026-09-30).
19. Pencil & Paper — Data Table UX Patterns (2026-02-23).
20. IBM Plex (2025-08-06).
21. MDN — `font-variant-numeric` (2026-09-10); `prefers-reduced-motion` (2026-06-10); `:focus-visible` (2026-10-16).

Caveat on sources: items 8–11 are vendor/industry trend content used descriptively, not as evidence of effectiveness. Items 2–4 predate 2025 by necessity — they are the canonical accessibility analyses of neumorphism, and no newer rebuttal exists because the style never returned to product UI.

## 8. Implementation order (completed)

1. Replaced the font `<link>` and deleted the `@import`; set `--font-ui/--font-data/--font-doc`. Verified: no FOUT beyond one swap, no render-blocking import.
2. Pasted the token block; deleted `--green*`, DM Sans/Manrope, and all `border-radius ≥ 8px`. Verified: no `border-radius: 8–12px` remains.
3. Converted the results view to the verdict block + checklist ledger before touching marketing surfaces. Verified: every criterion row shows a rule ID and a state word.
4. Added `:focus-visible`, `scroll-padding-top`, 24×24 minimum targets, and the reduced-motion block. Verified: tab through the whole flow with a sticky header, nothing hidden.
5. Restyled the hero and cut it to ≤ 40% of the first viewport so the upload surface is visible without scrolling.
