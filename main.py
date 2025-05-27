from SentimentModel import SentimentAnalyzerModel
from Database import ReviewDatabase

if __name__ == "__main__":

    # Inicjacja bazy i modelu
    db = ReviewDatabase()
    model = SentimentAnalyzerModel()

    while True:
        print("\nWybierz opcję:")
        print("1. Dodaj recenzję")
        print("2. Wyświetl recenzję")
        print("3. Usuń recenzje")
        print("4. Edytuj recenzję")
        print("5. Przeanalizuj sentyment recenzji")
        print("6. Wyjście")

        choice = input("Wybór: ")

        match choice:
            case '1':
                # Dodaj recenzję
                review = input("Wpisz swoją recenzję: ")
                db.insert_own_review(review)

            case '2':
                # wyświetl
                rows = db.select_all_data()
                for row in rows:
                    print(row)

            case '3':
                # usuń
                review_id = input("Podaj ID recenzji do usunięcia: ")
                db.delete_data(int(review_id))

            case '4':
                # edytuj
                review_id = input("Podaj ID recenzji do edycji: ")
                new_review = input("Wpisz nową treść recenzji: ")
                db.update_data_review(new_review, review_id)

            case '5':
                # analiza
                print("Rozpoczęto analizę...")
                reviews = db.select_all_data()

                # pętla po recenzjach
                for review in reviews:
                    # ID iterowanej recenzji
                    review_id = review[0]
                    # Pobranie recenzji o konkretnym ID
                    review_row = db.select_one_review(review_id)

                    if review_row:
                        # Analiza sentymentu recenzji
                        label, score = model.analyze(review_row[0])
                        print(f'Recenzja {review_id} '
                              f'o treści: {review_row}, '
                              f'wniosek: {label}, '
                              f'ocena: {score}')
                        # Zapisanie wyników analizy sentymentu do bazy danych
                        db.update_data_score_and_label(label, score, review_id)

                    else:
                        # Jeśli nie ma takiej recenzji
                        print(f'There is no review with id {review_id}')

            case '6':
                # wyjście
                print("Koniec działania programu.")
                break
