# Grundstruktur für das Kanban-Board
import json
from datetime import datetime
from enum import Enum


class Step(Enum):
    TODO = "ToDo"
    DOWNLOADS_ERFOLGT = "Downloads erfolgt"
    UPSCALING_ERFOLGT = "Upscaling erfolgt"
    EXCEL_ERSTELLT = "Excel erstellt"
    ARCHIVE = "Archiv"
    ERROR = "Fehler"


kanban_data = {
    Step.TODO.value: [],
    Step.DOWNLOADS_ERFOLGT.value: [],
    Step.UPSCALING_ERFOLGT.value: [],
    Step.EXCEL_ERSTELLT.value: [],
    Step.ARCHIVE.value: [],
    Step.ERROR.value: []
}


# Dateipfad zur Speicherung der Daten
data_file = "kanban_data.json"


# falls es keine Nischen gibt, wird im nächsten Step geprüft, ob es eine Nische gibt
def get_first_item():
    kanban = load_data()
    if kanban[Step.TODO.value]:
        return kanban[Step.TODO.value][0]
    elif kanban[Step.DOWNLOADS_ERFOLGT.value]:
        return kanban[Step.DOWNLOADS_ERFOLGT.value][0]
    elif kanban[Step.UPSCALING_ERFOLGT.value]:
        return kanban[Step.UPSCALING_ERFOLGT.value][0]
    elif kanban[Step.EXCEL_ERSTELLT.value]:
        return kanban[Step.EXCEL_ERSTELLT.value][0]
    elif kanban[Step.ARCHIVE.value]:
        return kanban[Step.ARCHIVE.value][0]
    else:
        return None


def set_download_success(niche):
    if niche in kanban_data[Step.TODO.value]:
        kanban_data[Step.TODO.value].remove(niche)
    kanban_data[Step.DOWNLOADS_ERFOLGT.value].append(niche)
    save_data()
    print(f"{datetime.now()}: Nische {niche} in {Step.DOWNLOADS_ERFOLGT.value} verschoben.")


def set_upscaling_success(niche):
    if niche in kanban_data[Step.DOWNLOADS_ERFOLGT.value]:
        kanban_data[Step.DOWNLOADS_ERFOLGT.value].remove(niche)
    kanban_data[Step.UPSCALING_ERFOLGT.value].append(niche)
    save_data()
    print(f"{datetime.now()}: Nische {niche} in {Step.UPSCALING_ERFOLGT.value} verschoben.")


def set_excel_success(niche):
    if niche in kanban_data[Step.UPSCALING_ERFOLGT.value]:
        kanban_data[Step.UPSCALING_ERFOLGT.value].remove(niche)
    kanban_data[Step.EXCEL_ERSTELLT.value].append(niche)
    save_data()


def set_archive(niche):
    kanban_data[Step.EXCEL_ERSTELLT.value].remove(niche)
    kanban_data[Step.ARCHIVE.value].append(niche)
    save_data()
    print(f"{datetime.now()}: Nische {niche} in {Step.ARCHIVE.value} verschoben.")


def set_error(niche):
    kanban_data(get_status_of_niche(niche)).remove(niche)
    kanban_data[Step.ERROR.value].append(niche)
    save_data()
    print(f"{datetime.now()}: Nische {niche} in {Step.ERROR.value} verschoben.")


def save_data():
    with open(data_file, 'w') as file:
        json.dump(kanban_data, file)


def add_task(niche):
    kanban_data[Step.TODO.value].append(niche)
    save_data()


def load_data():
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return kanban_data


def get_status_of_niche(niche):
    kanban = load_data()
    for step, niches in kanban.items():
        if niche in niches:
            return step
