import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Database import ReviewDatabase


@pytest.fixture
def db():
    db = ReviewDatabase('file::memory:?cache=shared')
    return db


def test_insert_own_review_and_select_all(db):
    db.insert_own_review("Testowa recenzja")
    rows = db.select_all_data()
    assert any("Testowa recenzja" in row for row in rows)


def test_update_data_review(db):
    db.insert_own_review("Stara recenzja")
    rows = db.select_all_data()
    review_id = rows[0][0]
    db.update_data_review("Nowa recenzja", review_id)

    updated_row = db.select_all_data()[0]
    assert "Nowa recenzja" in updated_row


def test_update_data_score_and_label(db):
    db.insert_own_review("Testowa analiza")
    review_id = db.select_all_data()[0][0]
    db.update_data_score_and_label("POSITIVE", 0.95, review_id)
    row = db.select_all_data()[0]
    assert row[2] == "POSITIVE"
    assert abs(row[3] - 0.95) < 1e-5


def test_delete_data(db):
    db.insert_own_review("Do usunięcia")
    review_id = db.select_all_data()[0][0]
    success = db.delete_data(review_id)
    assert success
    assert db.select_one_review(review_id) is None


def test_delete_nonexistent_review(db):
    success = db.delete_data(9999)
    assert not success


def test_update_nonexistent_review(db):
    success = db.update_data_review("Nieistniejąca", 9999)
    assert not success


def test_select_one_review(db):
    db.insert_own_review("Sprawdzana recenzja")
    review_id = db.select_all_data()[0][0]
    row = db.select_one_review(review_id)
    assert row is not None
    assert isinstance(row[0], str)
