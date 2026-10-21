"""Testing helper: make an island's decay clock look older.

Usage (run from the project folder, with your virtual environment active):
    python set_decay.py USERNAME ISLAND_SLOT DAYS_AGO [PROGRESS]

Examples:
    python set_decay.py test_user 1 3        # last decay was 3 days ago
    python set_decay.py test_user 1 3 5      # same, and set progress to 5 first
"""
import sys
from datetime import timedelta

from app import app, db, User, Island, UserIslandProgress, today_utc

if len(sys.argv) < 4:
    sys.exit(__doc__)

username = sys.argv[1].lower()
slot = int(sys.argv[2])
days_ago = int(sys.argv[3])
new_progress = int(sys.argv[4]) if len(sys.argv) > 4 else None

with app.app_context():
    user = User.query.filter_by(username=username).first()
    island = Island.query.filter_by(slot=slot).first()
    if user is None or island is None:
        sys.exit("No such user or island slot.")

    prog = UserIslandProgress.query.filter_by(user_id=user.id, island_id=island.id).first()
    if prog is None:
        sys.exit("That user has no progress row for this island.")

    prog.last_decay_date = today_utc() - timedelta(days=days_ago)
    if new_progress is not None:
        prog.progress = new_progress
    db.session.commit()

    print(f"{username} / island {slot}: progress={prog.progress}, "
          f"last_decay_date={prog.last_decay_date}")