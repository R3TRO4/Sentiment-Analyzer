import sqlite3


class ReviewDatabase:
    def __init__(self, db_path='review_database.db'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        print("Database has been initialized")
        self.create_table(self.cursor)
        self.insert_data(self.cursor)

    def create_table(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                FIND INTEGER PRIMARY KEY AUTOINCREMENT,
                REVIEW TEXT,
                LABEL TEXT,
                SCORE FLOAT
            ) """)
        print('Table reviews has been created.')

    def select_all_data(self, cursor):
        cursor.execute("SELECT * FROM reviews")
        return cursor.fetchall()

    def insert_own_review(self, cursor, review):
        cursor.execute(
            "INSERT INTO reviews (REVIEW) VALUES (?)",
            (review,)
        )
        print("\nNew review has been inserted.")

    def insert_data(self, cursor):
        cursor.execute(
            "INSERT INTO reviews (REVIEW) VALUES (?)",
            ("To był świetny film!",)
        )
        cursor.execute(
            "INSERT INTO reviews (REVIEW) VALUES (?)",
            ("To był beznadziejny film!",)
        )
        cursor.execute(
            "INSERT INTO reviews (REVIEW) VALUES (?)",
            ("To był w porządku film.",)
        )
        print('Data has been inserted.')

    def delete_data(self, cursor, review_id):
        cursor.execute(
            "SELECT 1 FROM reviews WHERE FIND = ?",
            (review_id,)
        )
        result = cursor.fetchone()
        if result:
            cursor.execute(
                "DELETE FROM reviews WHERE FIND = ?", (review_id,)
            )
            print(f'Review with ID {review_id} has been deleted.')
        else:
            print(f'Review with ID {review_id} was not found.')

    def update_data_review(self, cursor, new_review, review_id):
        cursor.execute(
            "SELECT 1 FROM reviews WHERE FIND = ?",
            (review_id,)
        )
        result = cursor.fetchone()
        if result:
            cursor.execute(
                "UPDATE reviews SET REVIEW = ? WHERE FIND = ?",
                (new_review, review_id)
            )
            print(f'Review with ID {review_id} has been updated.')
        else:
            print(f'Review with ID {review_id} was not found.')

    def update_data_score_and_label(self, cursor, label, score, review_id):
        cursor.execute(
            "UPDATE reviews SET LABEL = ?, SCORE = ? WHERE FIND = ? ",
            (label, score, review_id)
        )

    def select_one_review(self, cursor, review_id):
        cursor.execute("SELECT REVIEW FROM reviews WHERE FIND=?", (review_id,))
        return cursor.fetchone()

    def commit_changes(self):
        self.connection.commit()

    def close(self, cursor, sqlite_connection):
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
