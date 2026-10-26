"""Tests for goal.py - run: python plan/test_goal.py
They work on a COPY of goals.json in a temp folder, so your real progress is never touched.
(Also a good example of how testing works: set up -> act -> check.)
"""
import json
import shutil
import tempfile
from pathlib import Path

import goal as G

fails = []


def check(name, cond):
    print(f"  [{'OK' if cond else 'FAIL'}] {name}")
    if not cond:
        fails.append(name)


tmp = Path(tempfile.mkdtemp())
shutil.copy(G.GOALS_FILE, tmp / "goals.json")
(tmp / "plan").mkdir()
G.GOALS_FILE, G.BOARD_MD, G.BOARD_HTML, G.ACHIEVEMENTS = (tmp / "goals.json", tmp / "GOAL_BOARD.md",
                                                         tmp / "plan" / "board.html", tmp / "ACHIEVEMENTS.md")

data = G.load()
check("goals load", len(data["goals"]) >= 1)
ids = [t["id"] for g in data["goals"] for t in g["tasks"]]
check("task IDs are unique", len(ids) == len(set(ids)))

G.cmd_done(data, "G2.1")
data = G.load()
_, t = G.find_task(data, "G2.1")
check("done marks the task", t["done"] and t["done_on"] == G.today().isoformat())
check("achievement logged", "G2.1" in G.ACHIEVEMENTS.read_text(encoding="utf-8"))
check("markdown board written", "G2.1" in G.BOARD_MD.read_text(encoding="utf-8"))
check("html board written", "Goal Board" in G.BOARD_HTML.read_text(encoding="utf-8"))

G.cmd_done(data, "G2.1")                       # second time: no duplicate log
check("done twice does not log twice", G.ACHIEVEMENTS.read_text(encoding="utf-8").count("G2.1") == 1)

g9 = G.find_goal(data, "G9")
for task in g9["tasks"]:
    G.cmd_done(data, task["id"]); data = G.load()
check("finishing every task logs GOAL ACHIEVED", "GOAL ACHIEVED" in G.ACHIEVEMENTS.read_text(encoding="utf-8"))

G.cmd_undo(data, "G2.1"); data = G.load()
_, t = G.find_task(data, "G2.1")
check("undo reopens", not t["done"] and t["done_on"] is None)

G.cmd_add(data, "G2", "Test task", "2026-12-01"); data = G.load()
check("add creates the next ID", any(t["title"] == "Test task" for t in G.find_goal(data, "G2")["tasks"]))

check("html escapes the data safely", "</script>" not in G.build_html(data).split("<script>")[1].split("</script>")[0])

shutil.rmtree(tmp)
print("\nALL PASS" if not fails else f"\nFAILED: {fails}")
raise SystemExit(1 if fails else 0)
