import os
import sys
from datetime import datetime

import requests

import excel_product_finisher
import niche_management
from image_processor import process_images_in_folder
from midjouney_api_requests import imagine, job_status_retriever
from midjouney_api_requests.button_presser import press_upscale_button, press_button
import shutil

base_folder_path = None


def load_data():
    return niche_management.load_data()


def get_first_item():
    return niche_management.get_first_item()


def download_image(url, dateiname):
    file_path = create_folder_with_date(get_first_item())
    basis_pfad = os.path.join(file_path, dateiname)
    datei_erweiterung = ".png"
    downloads_pfad = f"{basis_pfad}{datei_erweiterung}"

    # Inkrementieren, falls die Datei bereits existiert
    counter = 1
    while os.path.exists(downloads_pfad):
        downloads_pfad = f"{basis_pfad}_{counter}{datei_erweiterung}"
        counter += 1

    response = requests.get(url)

    if response.status_code == 200:
        with open(downloads_pfad, 'wb') as file:
            file.write(response.content)
        print(f"{datetime.now()}: Das Bild wurde erfolgreich als {downloads_pfad} gespeichert.")
    else:
        print(f"{datetime.now()}: Fehler beim Herunterladen des Bildes.")


def process_image(initial_job_id, button_name):
    response_button_press = press_button(initial_job_id, button_name)
    if response_button_press is None or 'jobid' not in response_button_press:
        print(f"{datetime.now()}: Fehler beim Drücken von {button_name}.")
        return

    job_status_retriever.wait_for_image_completion(response_button_press.get("jobid"))
    response_image_details = job_status_retriever.fetch_job_details(response_button_press.get("jobid"))
    if response_image_details is None:
        print(f"{datetime.now()}: Fehler beim Abrufen der Bild-Details.")
        return
    print(response_image_details)

    response_upscale = press_upscale_button(response_button_press.get("jobid"))
    if response_upscale is None or 'jobid' not in response_upscale:
        print(f"{datetime.now()}: Fehler beim Starten des Upscaling.")
        return

    job_status_retriever.wait_for_image_completion(response_upscale.get("jobid"))
    response_finished_upscale = job_status_retriever.fetch_job_details(response_upscale.get("jobid"))
    if response_finished_upscale is None:
        print(f"{datetime.now()}: Fehler beim Abrufen der finalen Bild-Details.")
        return
    print(response_finished_upscale)

    attachments = response_finished_upscale.get("attachments")
    if attachments:
        url = attachments[0].get("url")
        if url:
            print(url)
            download_image(url, f"download")
        else:
            print(f"{datetime.now()}: Keine URL in den Attachments gefunden.")
    else:
        print(f"{datetime.now()}: Keine Attachments im Antwort-Objekt gefunden.")


def create_folder_with_date(todo_item_name):
    current_date = datetime.now().strftime("%Y%m%d")
    base_path = "/Users/maiklowen/1_Projects/T-Shirt Business"
    folder_name = f"{current_date}_{todo_item_name}"
    global base_folder_path
    base_folder_path = os.path.join(base_path, folder_name)

    if not os.path.exists(base_folder_path):
        os.makedirs(base_folder_path)
        print(f"{datetime.now()}: Ordner '{base_folder_path}' wurde erfolgreich erstellt.")
    else:
        print(f"{datetime.now()}: Ordner '{base_folder_path}' existiert bereits.")

    downloads_folder_path = os.path.join(base_folder_path, "downloads")
    if not os.path.exists(downloads_folder_path):
        os.makedirs(downloads_folder_path)
        print(f"{datetime.now()}: Unterordner 'downloads' wurde erfolgreich in '{base_folder_path}' erstellt.")
    else:
        print(f"{datetime.now()}: Unterordner 'downloads' existiert bereits in '{base_folder_path}'.")

    return downloads_folder_path


def get_base_folder_path(todo_item_name):
    current_date = datetime.now().strftime("%Y%m%d")
    base_path = "/Users/maiklowen/1_Projects/T-Shirt Business"
    folder_name = f"{current_date}_{todo_item_name}"
    global base_folder_path
    return os.path.join(base_path, folder_name)


def check_or_create_subfolder(parent_folder, subfolder_name):
    """
    Creates a subfolder within the specified parent folder and returns the path to this subfolder.

    :param parent_folder: The path to the parent folder where the subfolder will be created.
    :param subfolder_name: The name of the subfolder to create.
    :return: The path to the created or existing subfolder.
    """
    # Construct the full path to the new subfolder
    subfolder_path = os.path.join(parent_folder, subfolder_name)

    # Check if the subfolder already exists
    if not os.path.exists(subfolder_path):
        # Create the subfolder if it doesn't exist
        os.makedirs(subfolder_path)
        print(f"{datetime.now()}: Subfolder '{subfolder_name}' created at: {subfolder_path}")
    else:
        print(f"{datetime.now()}: Subfolder '{subfolder_name}' already exists.")

    return subfolder_path


def process_first_niche(picture_amount: int):
    todo_item = get_first_item()
    aktueller_status = niche_management.get_status_of_niche(todo_item)
    step = niche_management.Step
    base_folder_path = get_base_folder_path(todo_item)
    while aktueller_status != step.ARCHIVE.value:
        if aktueller_status == step.TODO.value:
            downloads_erstellen(picture_amount, todo_item)
            niche_management.set_download_success(todo_item)
        elif aktueller_status == step.DOWNLOADS_ERFOLGT.value:
            upscaling_starten(base_folder_path)
            niche_management.set_upscaling_success(todo_item)
        elif aktueller_status == step.UPSCALING_ERFOLGT.value:
            excel_erstellen(base_folder_path)
            niche_management.set_excel_success(todo_item)
        elif aktueller_status == step.EXCEL_ERSTELLT.value:
            downloads_ordner_loeschen(base_folder_path)
            niche_management.set_archive(todo_item)
        elif aktueller_status == step.ARCHIVE.value:
            print(f"{datetime.now()}: Nische wurde verarbeitet und archiviert.")
            sys.exit(0)
        aktueller_status = niche_management.get_status_of_niche(todo_item)
    if aktueller_status == step.ARCHIVE.value:
        print(f"{datetime.now()}: Nische {todo_item} wurde bereits verarbeitet und archiviert.")
        return
    else:
        print(f"{datetime.now()}: Nische {todo_item} konnte nicht verarbeitet werden.")
        niche_management.set_error(todo_item)


def downloads_erstellen(picture_amount, todo_item):
    image_description = "A cartoon logo of " + todo_item
    for _ in range(picture_amount):
        print(f"{datetime.now()}: Processing description: {image_description}...")
        # Sende die Beschreibung zur API und starte den Bildverarbeitungsprozess
        status_code, job_id = imagine.send_prompt_to_api(image_description)
        if status_code == 200:
            job_status_retriever.wait_for_image_completion(job_id)
            response_imagine_prompt = job_status_retriever.fetch_job_details(job_id)

            # Durchlaufe den Prozess für jeden Button
            for button in ['U1', 'U2', 'U3', 'U4']:
                print(f"{datetime.now()}: Processing image with button {button}...")
                process_image(response_imagine_prompt.get("jobid"), button)
        else:
            print(f"{datetime.now()}: Failed to process the description: {todo_item} with status code: {status_code}")


def upscaling_starten(base_folder_path):
    download_folder_path = check_or_create_subfolder(base_folder_path, "downloads")
    processed_images_folder_path = check_or_create_subfolder(base_folder_path, "processed_images")
    process_images_in_folder(download_folder_path, processed_images_folder_path)
    print(f"{datetime.now()}: All images processed.")


def excel_erstellen(base_folder_path):
    processed_images_folder_path = check_or_create_subfolder(base_folder_path, "processed_images")
    print(f"{datetime.now()}: Start creating Excel-File")
    print(processed_images_folder_path)
    print(get_first_item())
    print(f"{base_folder_path}/ImportExcel.xlsx")
    excel_product_finisher.edit_excel_sheet(processed_images_folder_path, get_first_item(), f"{base_folder_path}/ImportExcel.xlsx")


def downloads_ordner_loeschen(base_folder_path):
    download_folder_path = os.path.join(base_folder_path, "downloads")
    if os.path.exists(download_folder_path):
        shutil.rmtree(download_folder_path)
        print(f"{datetime.now()}: Der Ordner '{download_folder_path}' wurde erfolgreich gelöscht.")
    else:
        print(f"{datetime.now()}: Der Ordner '{download_folder_path}' existiert nicht.")


def main():
    process_first_niche(1)


if __name__ == "__main__":
    main()
