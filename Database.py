import sqlite3


class ReviewDatabase:
    def __init__(self, db_path='review_database.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path,
                                    check_same_thread=False,
                                    uri=True)
        self.cursor = self.conn.cursor()

        print("Zainicjowano połączenie z bazą danych.")
        self.create_table()
        self.insert_data()
        self.conn.commit()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                FIND INTEGER PRIMARY KEY AUTOINCREMENT,
                REVIEW TEXT,
                LABEL TEXT,
                SCORE FLOAT
            )
        """)

    def insert_data(self):
        self.cursor.execute(
            "INSERT INTO reviews (REVIEW) VALUES (?)",
            ("To był świetny film!",)
        )
        self.cursor.execute(
            "INSERT INTO reviews (REVIEW) VALUES (?)",
            ("To był beznadziejny film!",)
        )
        self.cursor.execute(
            "INSERT INTO reviews (REVIEW) VALUES (?)",
            ("To był w porządku film.",)
        )

    def insert_own_review(self, review):
        self.cursor.execute(
            "INSERT INTO reviews (REVIEW) VALUES (?)",
            (review,))
        self.conn.commit()
        print("✅ Recenzja została dodana.")

    def select_all_data(self):
        self.cursor.execute("SELECT * FROM reviews")
        return self.cursor.fetchall()

    def delete_data(self, review_id):
        self.cursor.execute(
            "SELECT 1 FROM reviews WHERE FIND = ?",
            (review_id,)
        )
        if self.cursor.fetchone():
            self.cursor.execute(
                "DELETE FROM reviews WHERE FIND = ?",
                (review_id,)
            )
            self.conn.commit()
            print(f"🗑️ Recenzja {review_id} została usunięta.")
            return True
        else:
            print(f"Nie znaleziono recenzji o ID {review_id}")
            return False

    def update_data_review(self, new_review, review_id):
        self.cursor.execute(
            "SELECT 1 FROM reviews WHERE FIND = ?",
            (review_id,)
        )
        if self.cursor.fetchone():
            self.cursor.execute(
                "UPDATE reviews SET REVIEW = ? WHERE FIND = ?",
                (new_review, review_id)
            )
            self.conn.commit()
            print(f"✅ Recenzja {review_id} została zaktualizowana.")
            return True
        else:
            print(f"Nie znaleziono recenzji o ID {review_id}")
            return False

    def update_data_score_and_label(self, label, score, review_id):
        self.cursor.execute(
            "UPDATE reviews SET LABEL = ?, SCORE = ? WHERE FIND = ?",
            (label, score, review_id)
        )
        self.conn.commit()

    def select_one_review(self, review_id):
        self.cursor.execute(
            "SELECT REVIEW FROM reviews WHERE FIND = ?",
            (review_id,))
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()
