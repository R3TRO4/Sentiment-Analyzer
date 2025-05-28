# Użyj oficjalnego obrazu z Pythonem 3.10 jako bazy
FROM python:3.10-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki z zależnościami i konfiguracją
COPY requirements.txt config.json ./

# Zainstaluj zależności aplikacji
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały kod źródłowy oraz testy
COPY . .

# Otwórz port Gradio (domyślny 7860)
EXPOSE 7860

# Domyślnie uruchamiaj aplikację (można nadpisać komendą)
CMD ["python", "app.py"]
