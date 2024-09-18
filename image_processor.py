# image_processor.py
import os

from PIL import Image
from rembg import remove


def process_image(input_path, output_path, new_size=(4500, 5400)):
    """
    Resizes an image, removes the background, and saves the processed image to output_path.
    """
    image = Image.open(input_path)
    old_size = image.size

    # Erstelle ein neues, größeres Bild mit weißem Hintergrund
    new_image = Image.new("RGB", new_size, (255, 255, 255))

    # Definiere den Abstand zum Rand
    offset = 200

    # Berechne die Position für das alte Bild, um es oben rechts im neuen Bild zu platzieren
    position = ((new_size[0] - old_size[0] - offset), offset)

    # Füge das alte Bild in das neue Bild ein
    new_image.paste(image, position)

    # Entferne den Hintergrund
    temp_path = output_path + '_temp.png'
    new_image.save(temp_path, format='PNG')
    with open(temp_path, 'rb') as input_file:
        input_image = input_file.read()
    output_image = remove(input_image)

    # Speichere das bearbeitete Bild
    with open(output_path, 'wb') as output_file:
        output_file.write(output_image)
    os.remove(temp_path)


def process_images_in_folder(input_folder, output_directory, new_size=(4500, 5400)):
    """
    Processes all images found in input_folder using process_image function.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_directory, os.path.splitext(file_name)[0] + '_processed.png')
            process_image(input_path, output_path, new_size)
            print(f"Processed {file_name}")
    print("All images processed.")
