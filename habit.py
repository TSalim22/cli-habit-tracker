"""Small habit tracker. All data stays in a local JSON file."""
import argparse
import json
from datetime import date, timedelta
from pathlib import Path


def load(path):
    if not path.exists():
        return []
    try:
        habits = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(habits, list):
            raise ValueError('Expected a list.')
        ids = set()
        for habit in habits:
            if not isinstance(habit, dict) or type(habit.get('id')) is not int or habit['id'] in ids:
                raise ValueError('Invalid habit ID.')
            ids.add(habit['id'])
            if not isinstance(habit.get('name'), str) or not habit['name'].strip():
                raise ValueError('Invalid name.')
            if not isinstance(habit.get('days'), list):
                raise ValueError('Invalid completion history.')
            for day in habit['days']:
                date.fromisoformat(day)
        return habits
    except (ValueError, TypeError, KeyError) as error:
        raise ValueError(f'Data file is invalid; it was not overwritten: {path}') from error


def save(path, habits):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(habits, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def streak(days, today=None):
    today = today or date.today()
    completed = {date.fromisoformat(day) for day in days}
    current = today if today in completed else today - timedelta(days=1)
    count = 0
    while current in completed:
        count += 1
        current -= timedelta(days=1)
    return count


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', type=Path, default=Path('data/habits.json'))
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('add', help='Add a habit')
    add.add_argument('name')
    commands.add_parser('list')
    commands.add_parser('stats')
    for command in ('check', 'uncheck', 'delete'):
        action = commands.add_parser(command)
        action.add_argument('id', type=int)
        if command == 'delete':
            action.add_argument('--yes', action='store_true', help='Confirm deletion')
        else:
            action.add_argument('--date', default=date.today().isoformat())
    args = parser.parse_args(argv)
    try:
        habits = load(args.file)
        if args.command == 'add':
            name = args.name.strip()
            if not name or len(name) > 80:
                raise ValueError('Habit names must contain 1–80 characters.')
            if any(h['name'].casefold() == name.casefold() for h in habits):
                raise ValueError('That habit already exists.')
            identifier = max((h['id'] for h in habits), default=0) + 1
            habits.append({'id': identifier, 'name': name, 'days': []})
            print(f'Added #{identifier}: {name}')
        elif args.command in ('list', 'stats'):
            if not habits:
                print('No habits yet. Add one with: python habit.py add "Read"')
            for habit in habits:
                status = 'done' if date.today().isoformat() in habit['days'] else 'pending'
                print(f"#{habit['id']} {habit['name']} | today: {status} | streak: {streak(habit['days'])} | total: {len(set(habit['days']))}")
            return 0
        else:
            habit = next((h for h in habits if h['id'] == args.id), None)
            if not habit:
                raise ValueError('Habit ID not found.')
            if args.command == 'delete':
                if not args.yes:
                    raise ValueError('Add --yes to confirm deleting the habit and its history.')
                habits.remove(habit)
            else:
                day = date.fromisoformat(args.date)
                if day > date.today():
                    raise ValueError('Cannot record a future day.')
                day = day.isoformat()
                if args.command == 'check' and day not in habit['days']:
                    habit['days'].append(day)
                    habit['days'].sort()
                elif args.command == 'uncheck' and day in habit['days']:
                    habit['days'].remove(day)
            print('Saved.')
        save(args.file, habits)
        return 0
    except (ValueError, OSError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
