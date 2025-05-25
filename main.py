from SentimentModel import SentimentAnalyzerModel
from Database import ReviewDatabase

if __name__ == "__main__":

    # Inicjacja bazy i modelu
    db = ReviewDatabase()
    model = SentimentAnalyzerModel()

    # Załadowanie wszystkich recenzji do listy
    reviews = db.select_all_data(db.cursor)

    # pętla po recenzjach
    for review in reviews:
        # ID iterowanej recenzji
        review_id = review[0]
        # Pobranie recenzji o konkretnym ID
        review_row = db.select_one_review(db.cursor, review_id)

        if review_row:
            # Analiza sentymentu recenzji
            label, score = model.analyze(review_row[0])
            print(review_id, label, score)
            # Zapisanie wyników analizy sentymentu do bazy danych
            db.update_data(db.cursor, label, score, review_id)
            # Zacommitowanie zmian
            db.commit_changes()

        else:
            # Jeśli nie ma takiej recenzji
            print(f'There is no review with id {review_id}')
