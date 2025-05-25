import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from Database import ReviewDatabase


@pytest.fixture
def db():
    # Tworzenie tymczasowej bazy danych w pamięci
    database = ReviewDatabase(':memory:')
    yield database
    database.connection.close()


def test_insert_and_select(db):
    db.insert_data(db.cursor)
    rows = db.select_all_data(db.cursor)
    assert len(rows) > 0


def test_update_data(db):
    db.insert_data(db.cursor)
    rows = db.select_all_data(db.cursor)
    review_id = rows[0][0]
    db.update_data(db.cursor, 'POSITIVE', 0.95, review_id)
    db.connection.commit()

    updated_row = db.select_all_data(db.cursor)[0]
    assert updated_row[2] == 'POSITIVE'
    assert abs(updated_row[3] - 0.95) < 0.0001


def test_delete_data(db):
    # Wstaw dane
    db.insert_data(db.cursor)
    db.connection.commit()

    # Pobierz dane i sprawdź, że coś jest
    rows = db.select_all_data(db.cursor)
    assert len(rows) > 0

    # Weź ID pierwszej recenzji i usuń ją
    review_id = rows[0][0]
    db.delete_data(db.cursor, review_id)
    db.connection.commit()

    # Sprawdź, że recenzja z tym ID już nie istnieje
    deleted_row = db.select_one_review(db.cursor, review_id)
    assert deleted_row is None


def test_select_one_review(db):
    db.insert_data(db.cursor)
    db.connection.commit()
    rows = db.select_all_data(db.cursor)
    review_id = rows[1][0]

    result = db.select_one_review(db.cursor, review_id)
    assert result is not None
    assert isinstance(result[0], str)


def test_delete_nonexistent_review(db):
    db.delete_data(db.cursor, 9999)  # Brak wyjątku to sukces
    db.connection.commit()


def test_update_nonexistent_review(db):
    db.update_data(db.cursor, 'NEGATIVE', 0.12, 9999)  # brak błędu to OK
    db.connection.commit()
    # Sprawdź, że nikt nie został zmodyfikowany
    rows = db.select_all_data(db.cursor)
    assert all(row[2] is None for row in rows)


def test_close(db):
    try:
        db.close(db.cursor, db.connection)
    except Exception as e:
        pytest.fail(f"Zamknięcie bazy danych nie powiodło się: {e}")
