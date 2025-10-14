import json
from datetime import date
import pytest
from habit import main, load, streak


def test_cli_roundtrip(tmp_path):
    path = tmp_path / 'habits.json'
    prefix = ['--file', str(path)]
    main(prefix + ['add', 'Read'])
    main(prefix + ['check', '1'])
    main(prefix + ['check', '1'])
    assert len(load(path)[0]['days']) == 1
    main(prefix + ['uncheck', '1'])
    assert load(path)[0]['days'] == []
    main(prefix + ['delete', '1', '--yes'])
    assert load(path) == []


def test_streak_counts_yesterday_when_today_pending():
    assert streak(['2026-01-01', '2026-01-02'], date(2026, 1, 3)) == 2
    assert streak(['2026-01-01'], date(2026, 1, 4)) == 0


def test_corrupt_data_is_preserved(tmp_path):
    path = tmp_path / 'broken.json'
    path.write_text('{broken')
    with pytest.raises(SystemExit):
        main(['--file', str(path), 'add', 'Read'])
    assert path.read_text() == '{broken'


def test_duplicates_and_future_dates_rejected(tmp_path):
    prefix = ['--file', str(tmp_path / 'habits.json')]
    main(prefix + ['add', 'Read'])
    with pytest.raises(SystemExit):
        main(prefix + ['add', 'read'])
    with pytest.raises(SystemExit):
        main(prefix + ['check', '1', '--date', '9999-01-01'])
