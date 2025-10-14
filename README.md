# CLI Habit Tracker

Track daily habits and streaks in a local JSON file.

This is a small, independent Python portfolio project. The code favours ordinary functions and clear modules over complex architecture.

## Setup

Requires Python 3.12+ (desktop tools also require Tkinter, included with the standard Windows Python installer).

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux instead: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python habit.py --help
```

Run commands from this repository's root. Web apps bind to localhost by default. Each app is independent, so stop one before starting another on the same port.

## Check it

```sh
python -m pytest -q
```

## Dates

The commit author dates have been deliberately arranged between October 2025 and October 2026 at the portfolio owner's request. They are presentation metadata, not a record of the actual development timeline. Repository creation and upload timestamps remain the real dates.

## Example session

```sh
python habit.py add "Read for 20 minutes"
python habit.py add "Practice Python"
python habit.py list
python habit.py check 1
python habit.py check 2 --date 2026-10-01
python habit.py stats
python habit.py uncheck 1
python habit.py delete 2 --yes
```

You can use a different data file: `python habit.py --file data/study.json add "Revise SQL"`. Dates must be today or earlier. Checking the same habit twice on the same day does not double-count it. A current streak may end today or yesterday, so an unfinished today does not immediately break it. Damaged JSON is reported without overwriting it. This is a single-user CLI; it does not coordinate simultaneous writers.

## Command demonstration

![Recorded CLI demonstration](docs/demo.gif)

The animation was generated from real command output using disposable sample data.
