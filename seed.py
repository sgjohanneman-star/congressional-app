from app import app, db, Island, Question
from seed_data import ISLANDS


def seed():
    for island_data in ISLANDS:
        island = Island.query.filter_by(slot=island_data["slot"]).first()
        if island is None:
            island = Island(slot=island_data["slot"])
            db.session.add(island)
        island.name = island_data["name"]
        island.description = island_data["description"]
        db.session.flush()

        for q in island_data["questions"]:
            choices = q["choices"]
            if len(choices) < 2:
                raise ValueError(f"Too few choices: {q['text']}")
            if not 0 <= q["correct"] < len(choices):
                raise ValueError(f"'correct' index out of range: {q['text']}")

            question = Question.query.filter_by(island_id=island.id, text=q["text"]).first()
            if question is None:
                question = Question(island_id=island.id, text=q["text"])
                db.session.add(question)
            question.choices = choices
            question.correct_answer = q["correct"]

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        try:
            seed()
            print("Seeding completed.")
        except Exception:
            db.session.rollback()
            print("Seeding failed.")
            raise