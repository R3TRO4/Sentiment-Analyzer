# Sentiment Analyzer

Projekt oparty na modelu językowym do analizy sentymentu tekstów (np. recenzji filmowych).  
Wykorzystuje model Hugging Face `tabularisai/multilingual-sentiment-analysis` oraz bazę SQLite do przechowywania recenzji i wyników.  
Jest testowany przy użyciu `pytest`, a interfejs webowy został zbudowany z wykorzystaniem biblioteki Gradio.

## Jak uruchomić projekt lokalnie

1. **Zainstaluj zależności:**

   Upewnij się, że masz zainstalowanego Pythona w wersji 3.10 i `pip`. Następnie w katalogu głównym projektu wykonaj:

   ```bash
   pip install -r requirements.txt

2. **Uruchom aplikację**

    Aby uruchomić aplikację, po zainstalowaniu wszystkich potrzebnych zależności, w katalogu głównym projektu wykonaj:

    ```bash
    python app.py
    ```
    Po uruchomieniu interfejs Gradio będzie dostępny pod adresem https://localhost:7860 (domyślny port Gradio)


3. **Uruchomienie aplikacji w konsoli (opcjonalnie)**
    
    Aby uruchomić aplikację w konsoli zamiast w interfejsie Gradio, wystarczy wykonać komendę:
    
    ```bash
    python main.py   
    ```
   
## Jak zbudować i uruchomić obraz Dockera

1. **Budowanie obrazu Dockera**

    W katalogu głównym projektu (tam gdzie znajduje się Dockerfile) uruchom komendę:

    ```bash
    docker build -t <tag-obrazu>
    ```

2. **Uruchomienie kontenera**

    Po zbudowaniu obrazu Dockera uruchom kontener komendą
    
    ```bash
    docker run -it --rm -p <port-hosta>:<port-kontenera> <tag-obrazu>
    ```
    gdzie:
    
    **-it** - zezwala na wyświetlanie printów w konsoli w trakcie działania aplikacji.

    **--rm** - po zakończeniu działania aplikacji, kontener jest usuwany.

    **-p** - mapowanie portów między hostem (komputerem) a kontenerem Dockera. Jeśli chcemy połączyć się z aplikacją na domyślnym porcie, komenda powinna wyglądać tak:
    
   ```bash
    docker run -it --rm -p 7860:7860 <tag-obrazu>
    ```
    Aplikacja będzie dostępna w przeglądarce pod adresem: http://localhost:7860


3. **Podstawowe komendy Dockera**
    
    Aby wyświetlić listę wszystkich obrazów zapisanych lokalnie na Twoim systemie użyj komendy:
    ``` bash
    docker images
    ```
    Aby wyświetlić listę wszystkich kontenerów, zarówno tych działających jak i zatrzymanych użyj komendy:
    
    ``` bash
    docker ps -a
   ```
   
    Aby usunąć kontener użyj komendy:
    ``` bash
    docker rm <id-kontenera>
    ```
   
    Aby usunąć obraz użyj komendy:
    ``` bash
   docker rmi <tag-obrazu>
   ```
