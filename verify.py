#!/usr/bin/env python3
"""closing-desk: dataTable, spreadsheet, gantt, calendar, kanban and tree report edits; the document decides what they mean."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
from appplayer import AppPlayer  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, "captures")
BUNDLE = os.path.join(HERE, "closing_desk.mbd")

ap = AppPlayer()
bid = ap.install_bundle(BUNDLE)
ap.restart()
ap.open_bundle(bid)
ap.wait_text("Closing sheet")
ap.wait_text("Balance due")
ap.expect_text("4231.52")
ap.shot(f"{CAP}/01_sheet.png")
hdr = [r for t, r in ap.texts("Amount ($)") if t == "Amount ($)"][0]
ap.tap_at(hdr[0] + hdr[2] / 2, hdr[1] + hdr[3] / 2)         # sort by amount
time.sleep(3)
x0 = hdr[0] - 8 - (230 + 120 + 70 + 70 + 120)
y0 = hdr[1] + hdr[3] + 12
# Ascending by amount, the last of the eight rows is the largest amount: Cabinet
# carcasses, 12 × 180 = 2160. The edit must name that row, not the row that sat
# at position 8 before the sort (Skip hire) — and the sort must be numeric: a
# 617.5 among integers is still smaller than 2160.
ap.tap_at(x0 + 350 + 35, y0 + 36 * 7 + 18)
time.sleep(0.5)
ap.type("14")
ap.wait_text("Cabinet carcasses · qty 12 → 14")
# Second edit, a rate this time: Wall tiling sits at row 5 of the ascending sort (617.5).
ap.tap_at(x0 + 490 + 60, y0 + 36 * 4 + 18)
time.sleep(0.5)
ap.type("98")
ap.wait_text("Wall tiling · rate 95 → 98")
ap.expect_text("EDITS REPORTED · 2")
ap.expect_text("4231.52")                                     # the settlement did not move: edits were reported, not applied
ap.shot(f"{CAP}/02_sheet_sorted_and_edited.png")
ap.tap("Programme →")
ap.wait_text("Snagging")
ap.shot(f"{CAP}/03_plan.png")
day = [r for t, r in ap.texts("18") if r[1] > 450][-1]
ap.tap_at(day[0] + 6, day[1] + 10)
ap.wait_text("Day 2026-09-18")
# A card from To do into In progress: the board reports the move, the document applies it.
card = ap.rect("Order splashback glass")
col = ap.rect("In progress")
ap.drag(card[0] + card[2] / 2, card[1] + card[3] / 2, col[0] + col[2] / 2, col[1] + 30)
ap.wait_text("Order splashback glass: todo #0 → doing #0")
moved = ap.rect("Order splashback glass")
assert moved[0] >= col[0] - 10, f"the board reported the move but the card stayed at x={moved[0]} (optimistic: true)"
# A node onto another: dropped inside, not reordered beside.
hood = ap.rect("Extractor hood")
run = ap.rect("Cabinet run")
ap.drag(hood[0] + hood[2] / 2, hood[1] + hood[3] / 2, run[0] + run[2] / 2, run[1] + run[3] / 2)
ap.wait_text("Extractor hood dropped inside Cabinet run")
# A bar on the gantt: t5 is the Carcasses row.
lab = ap.rect("Carcasses")
ap.tap_at(475, lab[1] + lab[3] / 2)
ap.wait_text("Task t5 selected")
ap.shot(f"{CAP}/04_plan_interacted.png")
print("closing-desk: an edit after a sort names its row; gantt, calendar, board and tree drawn from state")
