import streamlit as st
from Database import ReviewDatabase
from SentimentModel import SentimentAnalyzerModel

# Inicjalizacja bazy i modelu
db = ReviewDatabase()
model = SentimentAnalyzerModel()

st.title("Analiza Sentymentu Recenzji")

# Pobranie danych z bazy
reviews = db.select_all_data(db.cursor)

# Wyświetlenie danych przed analizą
st.subheader("📋 Dane przed analizą")
st.table(reviews)

# Przycisk do analizy
if st.button("Analizuj sentyment"):
    for review in reviews:
        review_id = review[0]
        review_text = review[1]

        if review_text:
            label, score = model.analyze(review_text)
            db.update_data_score_and_label(db.cursor, label, score, review_id)

    st.success("Analiza zakończona ✅")

    # Odśwież dane po analizie
    updated_reviews = db.select_all_data(db.cursor)

    st.subheader("📊 Dane po analizie")
    st.table(updated_reviews)

# Zamknięcie bazy
db.connection.commit()
