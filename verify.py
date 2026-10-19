from sqlalchemy.exc import IntegrityError
from app import app, db, Island, Question, User, UserIslandProgress

with app.app_context():
    for island in Island.query.order_by(Island.slot):
        print(f"Slot {island.slot}: {island.name} - {len(island.questions)} questions")
    print("Total:", Island.query.count(), "islands,", Question.query.count(), "questions")

    user = User(username="verify_user", password_hash="not-a-real-hash")
    db.session.add(user)
    db.session.commit()

    island = Island.query.first()
    db.session.add(UserIslandProgress(user_id=user.id, island_id=island.id))
    db.session.commit()

    db.session.add(UserIslandProgress(user_id=user.id, island_id=island.id))
    try:
        db.session.commit()
        print("FAIL: duplicate row was allowed")
    except IntegrityError:
        db.session.rollback()
        print("PASS: duplicate row rejected")

    UserIslandProgress.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()