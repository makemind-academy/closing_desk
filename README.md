# closing-desk — an interior contractor's closing desk

One app, two routes. Everything the widgets do is *reported* to the document; no widget rewrites
its own data.

| route | widgets | what it shows |
|---|---|---|
| `/sheet` | `dataTable` (`editable`, `onCellEdit`, `onRowTap`) · `spreadsheet` (`formulas: true`) | Job lines with editable qty/rate. A settlement strip whose cells are formulas over the page state (`contractSum + variations - round(...) - deposit`). Every committed edit lands in `edits[]` and the footer. |
| `/plan` | `gantt` (groups, progress, `onTaskClick`) · `calendar` (events, `onChange`) · `kanban` (`itemTemplate`, `onCardMove`, `optimistic`) · `tree` (`draggable`, `onDrop` → before / inside / after) | The programme, the site calendar, the board and the room tree. Card moves and node drops are reported with their destination. |

## Run it

AppPlayer → `Add app → Bundle → Folder` → pick `closing_desk.mbd/`.

## Verified on

`flutter_mcp_ui_runtime 0.7.8` (local cut, 2026-09-04, not yet published — path override on an AppPlayer Standard debug
build) · `flutter_mcp_ui_core 0.6.5` · `appplayer_core 0.1.27`. Captures in `captures/` are the debug host's own
`ui.screenshot` at 1280×868. `_0.7.7/` keeps the captures from the published 0.7.7, `_0.7.8-prepub/` the raw
measurement frames.

| capture | what happened before it |
|---|---|
| `01_sheet.png` | fresh open (rows sorted by `sortColumn: trade` from state) |
| `02_sheet_sorted_and_edited.png` | *Amount* header tapped (`onSort` → rows reorder), then qty 12→14 on *Cabinet carcasses* and rate 95000→98000 on *Wall tiling* — both reported through `onCellEdit` naming the row on screen, table rows unchanged by the widget |
| `03_plan.png` | fresh open — dependency arrows drawn, done fraction in the bar colour |
| `04_plan_interacted.png` | calendar day 18 tapped (`event.value` = `2026-09-18`) · gantt bar t5 tapped · card *Order splashback glass* dragged todo #0 → doing #2 · node *Extractor hood* dropped **inside** *Cabinet run* |

## What was measured on the published 0.7.7 and fixed in 0.7.8

Reported 2026-09-04 and fixed the same day; the document is written to the spec and carries no workaround.

- `dataTable.editable` only took effect on the `virtualScroll` / `resizableColumns` path, and that path had no header sort. 0.7.8 edits on the default path, sorts by header tap, and keys cells by row identity so an edit after a sort names the row on screen.
- `gantt.showDependencies` drew nothing. 0.7.8 draws elbowed arrows. Progress fill was the lighter tint over the done fraction; now the bar colour.
- `tree`: expandable nodes were neither drag sources nor drop targets, so `inside` was unreachable.
- `calendar.onChange` `event.value` carried a time component.
