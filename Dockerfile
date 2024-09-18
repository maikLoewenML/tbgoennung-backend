# Verwende ein offizielles Python-Image als Basis
FROM python:3.9

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere System-Abhängigkeiten
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiere die Anforderungen-Datei und installiere die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Anwendungscodes
COPY . .

# Exponiere den Port, auf dem die App läuft
EXPOSE 5000

# Definiere den Befehl zum Starten der Anwendung
CMD ["python", "app.py"]
