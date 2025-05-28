import gradio as gr
from SentimentModel import SentimentAnalyzerModel
from Database import ReviewDatabase

# Inicjalizacja bazy i modelu
db = ReviewDatabase()
model = SentimentAnalyzerModel()

# Funkcja: dodaj recenzję
def add_review(review_text):
    if not review_text.strip():
        return "⚠️ Wpisz recenzję!"
    db.insert_own_review(review_text)
    return "✅ Recenzja została dodana."

# Funkcja: pokaż wszystkie recenzje
def show_reviews():
    rows = db.select_all_data()
    if not rows:
        return "Brak recenzji."
    return "\n\n".join([f"ID: {r[0]}\nRecenzja: {r[1]}\nSentyment: {r[2]}\nOcena: {r[3]}" for r in rows])

# Funkcja: edytuj recenzję
def edit_review(review_id, new_text):
    if db.update_data_review(new_text, review_id):
        return f"✅ Recenzja {review_id} została zaktualizowana."
    else:
        return f"❌ Nie znaleziono recenzji o ID {review_id}."

# Funkcja: usuń recenzję
def delete_review(review_id):
    if db.delete_data(int(review_id)):
        return f"🗑️ Recenzja {review_id} została usunięta."
    else:
        return f"❌ Nie znaleziono recenzji o ID {review_id}."

# Funkcja: analiza sentymentu
def sentiment_analyzer():
    reviews = db.select_all_data()
    output = []
    for review in reviews:
        review_id = review[0]
        review_text = review[1]
        label, score = model.analyze(review_text)
        db.update_data_score_and_label(label, score, review_id)
        output.append(f"ID: {review_id}\nTreść: {review_text}\nSentyment: {label}, Score: {score:.2f}")
    return "\n\n".join(output)

# Interfejs Gradio
with gr.Blocks(title="Analiza Sentymentu") as demo:
    gr.Markdown("# 🎬 Analiza Sentymentu Recenzji Filmowych")

    with gr.Tab("Dodaj recenzję"):
        review_input = gr.Textbox(label="Wpisz recenzję")
        add_output = gr.Textbox(label="Status")
        add_button = gr.Button("Dodaj")
        add_button.click(fn=add_review, inputs=review_input, outputs=add_output)

    with gr.Tab("Pokaż recenzje"):
        view_output = gr.Textbox(label="Recenzje", lines=20)
        view_button = gr.Button("Odśwież")
        view_button.click(fn=show_reviews, outputs=view_output)

    with gr.Tab("Edytuj recenzję"):
        edit_id = gr.Number(label="ID recenzji", precision=0)
        new_text = gr.Textbox(label="Nowa treść")
        edit_output = gr.Textbox(label="Status")
        edit_button = gr.Button("Zaktualizuj")
        edit_button.click(fn=edit_review, inputs=[edit_id, new_text], outputs=edit_output)

    with gr.Tab("Usuń recenzję"):
        delete_id = gr.Number(label="ID recenzji do usunięcia", precision=0)
        delete_output = gr.Textbox(label="Status")
        delete_button = gr.Button("Usuń")
        delete_button.click(fn=delete_review, inputs=delete_id, outputs=delete_output)

    with gr.Tab("Analiza sentymentu"):
        analyze_output = gr.Textbox(label="Wyniki analizy", lines=20)
        analyze_button = gr.Button("Analizuj wszystkie recenzje")
        analyze_button.click(fn=sentiment_analyzer, outputs=analyze_output)

# Uruchomienie aplikacji
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
