import os
import time

import gemini_api_requester
import pandas as pd


def create_product_description_200_characters(nische: str) -> str:
    question = (f"Erstelle eine Beschreibung für diese Nische: {nische}, die 200 Zeichen lang ist. Die Beschreibung "
                f"sollte nicht das Wort Geschenkidee enthalten. Falls irgendwelche Wörter in dem Text trademarkgeschützt sind, "
                f"will ich, dass du diese rauslässt und nicht für die Beschreibung nutzt. Die Beschreibung sollte nicht für irgendein Produkt sein "
                f"Es soll nur eine Beschreibung über diese Nische sein und den Leser inspirieren!")
    return gemini_api_requester.generate_text_safety_config("gmail-mail-deleter", "europe-west3", question)


def create_product_description_250_characters(nische: str) -> str:
    question = (f"Erstelle eine Beschreibung für diese Nische: {nische}, die 250 Zeichen lang ist. Die Beschreibung "
                f"sollte nicht das Wort Geschenkidee enthalten. Falls irgendwelche Wörter in dem Text trademarkgeschützt sind, "
                f"will ich, dass du diese rauslässt und nicht für die Beschreibung nutzt. Die Beschreibung sollte nicht für irgendein Produkt sein "
                f"Es soll nur eine Beschreibung über diese Nische sein und den Leser inspirieren!")
    return gemini_api_requester.generate_text_safety_config("gmail-mail-deleter", "europe-west3", question)


def create_product_description_500_characters(nische: str) -> str:
    question = (f"Erstelle eine Beschreibung für diese Nische: {nische}, die 500 Zeichen lang ist. Die Beschreibung "
                f"sollte nicht das Wort Geschenkidee enthalten. Falls irgendwelche Wörter in dem Text trademarkgeschützt sind, "
                f"will ich, dass du diese rauslässt und nicht für die Beschreibung nutzt. Die Beschreibung sollte nicht für irgendein Produkt sein "
                f"Es soll nur eine Beschreibung über diese Nische sein und den Leser inspirieren!")
    return gemini_api_requester.generate_text_safety_config("gmail-mail-deleter", "europe-west3", question)


def create_50_tags(nische: str) -> str:
    question = "Erstelle 50 tags für die Nische: " + str(nische) + (". Die Tags sollte komma-separiert sein und nicht als aufgezählte Liste dargestellt "
                                                                    "werden. Außerdem sollten die Tags nicht trademarkgeschützt sein, sondern frei verfügbar. "
                                                                    "Die Tags sollten die Suchmaschinenoptimierung verbessern.")
    return gemini_api_requester.generate_text_safety_config("gmail-mail-deleter", "europe-west3", question)


def edit_excel_sheet(directory_path, niche, output_file_path: str):
    try:
        input_file_path = "/Users/maiklowen/3_Resources/T-Shirt Business Gönnung/FlyingUploadMBA.xlsx"
        df = pd.read_excel(input_file_path)
        df['Index'] = range(1, len(df) + 1)  # Erstelle einen expliziten 'Index' wenn nötig
        image_paths = []

        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            # Überprüfe, ob der Dateipfad auf eine Datei zeigt und eine typische Bilddateierweiterung hat
            if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(file_path)

        tags = create_50_tags(niche)
        description = create_product_description_200_characters(niche)
        bullet_point_1 = create_product_description_250_characters(niche)
        bullet_point_2 = create_product_description_250_characters(niche)

        if not image_paths:
            print("Keine Bilddateien gefunden.")
            return

        products = ['Standard t-shirt', 'Premium t-shirt', 'V-neck t-shirt', 'Tank top', 'Long sleeve t-shirt', 'Raglan', 'Sweatshirt', 'Pullover hoodie',
                    'Zip hoodie', 'PopSockets grip', 'iphone_cases', 'samsung_cases', 'tote_bag', 'throw_pillows']
        price_dict = {
            'Standard t-shirt': '19.99',
            'Premium t-shirt': '19.99',
            'V-neck t-shirt': '19.99',
            'Tank top': '19.99',
            'Long sleeve t-shirt': '19.99',
            'Raglan': '19.99',
            'Sweatshirt': '29.99',
            'Pullover hoodie': '34.99',
            'Zip hoodie': '29.99',
            'PopSockets grip': '14.99',
            'iphone_cases': '17.99',
            'samsung_cases': '17.99',
            'tote_bag': '19.99',
            'throw_pillows': '19.99'
        }
        new_rows_list = []
        print(image_paths)

        for image_path in image_paths:
            for product in products:
                color = 'black_athletic_heather' if product == 'Raglan' else 'black'
                new_row = {
                    'Image Path': image_path,
                    'Input Language': 'DE',
                    'Title': niche,
                    'Description': description,
                    'Tags': tags,
                    'Type': 'man, woman, youth',
                    'Color': color,
                    'Brand': f"{niche} Lovers",
                    'Bullet Points 1': bullet_point_1,
                    'Bullet Points 2': bullet_point_2,
                    'Color1': 'black',
                    'Product': product,
                    'Marketplace': 'DE, US, GB, IT, ES, FR, JP',
                    'Price US': price_dict[product],
                    'Price GB': price_dict[product],
                    'Price DE': price_dict[product],
                    'Price FR': price_dict[product],
                    'Price IT': price_dict[product],
                    'Price ES': price_dict[product],
                    'Price JP': '5000',
                    'Auto Translate': 'yes'
                }
                print(new_row)
                new_rows_list.append(new_row)
            time.sleep(30)

        # Erstelle einen neuen DataFrame aus der Liste der neuen Zeilen
        if new_rows_list:  # Überprüfe, ob die Liste nicht leer ist
            new_rows_df = pd.DataFrame(new_rows_list)
            df = pd.concat([df, new_rows_df], ignore_index=True)

        df.to_excel(output_file_path, index=False)
        print(f"Datei erfolgreich gespeichert: {output_file_path}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def main():
    """
    print("200 Char Description: " + create_product_description_200_characters("Home is where your beagle is") + "\n")
    print("250 Char Description: " + create_product_description_250_characters("Home is where your beagle is") + "\n")
    print("250 Char Description: " + create_product_description_250_characters("Home is where your beagle is") + "\n")
    print("500 Char Description: " + create_product_description_500_characters("Home is where your beagle is") + "\n")
    print("50 Tags: " + create_50_tags("Home is where your beagle is"))
    edit_excel_sheet("/Users/maiklowen/1_Projects/T-Shirt Business/20240409_I was the boss until I got a beagle/processed_images", "I was the boss until I got a beagle",
                     f"/Users/maiklowen/1_Projects/T-Shirt Business/20240409_I was the boss until I got a beagle/ImportExcel.xlsx")

    translator = Translator()
    result = translator.translate(
        'Obwohl er wusste, dass der von ihm in der Diskussion vorgebrachte, reichlich mit Fachjargon gespickte Standpunkt schwer verständlich sein könnte, beharrte er dennoch darauf, um die Tiefe seines Verständnisses des Themas zu unterstreichen.',
        dest='en')
    print(result.text)"""


if __name__ == "__main__":
    main()
