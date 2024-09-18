import tkinter as tk
from tkinter import simpledialog, messagebox
import json

# Grundstruktur für das Kanban-Board
kanban_data = {
    "ToDo": [],
    "Done": [],
    "Archiv": []
}

# Dateipfad zur Speicherung der Daten
data_file = "kanban_data.json"


def save_data():
    with open(data_file, 'w') as file:
        json.dump(kanban_data, file)


def load_data():
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return kanban_data


def add_task():
    task = simpledialog.askstring("Nische", "Beschreiben Sie die Nische:")
    if task:
        kanban_data["ToDo"].append(task)
        update_board()
        save_data()


def move_task(task, from_column, to_column):
    if task and task in kanban_data[from_column]:
        kanban_data[from_column].remove(task)
        kanban_data[to_column].append(task)
        update_board()
        save_data()
    else:
        print(f"Nische '{task}' nicht in Spalte '{from_column}' gefunden oder keine Nische ausgewählt.")


def delete_task(task, from_column):
    if task and task in kanban_data[from_column]:
        if messagebox.askyesno("Nische löschen", f"Sind Sie sicher, dass Sie '{task}' löschen möchten?"):
            kanban_data[from_column].remove(task)
            update_board()
            save_data()


def update_board():
    for column in columns:
        columns[column].delete(0, tk.END)
        for task in kanban_data[column]:
            columns[column].insert(tk.END, task)


def create_buttons(frame, column):
    if column == "ToDo":
        add_button = tk.Button(frame, text="Nische hinzufügen", command=add_task)
        add_button.pack(pady=5)
        move_button = tk.Button(frame, text="Verschiebe nach Done",
                                command=lambda: move_task(columns["ToDo"].get(tk.ANCHOR), "ToDo", "Done"))
        move_button.pack(pady=5)
    elif column == "Done":
        move_button = tk.Button(frame, text="Verschiebe nach Archiv",
                                command=lambda: move_task(columns["Done"].get(tk.ANCHOR), "Done", "Archiv"))
        move_button.pack(pady=5)
    elif column == "Archiv":
        delete_button = tk.Button(frame, text="Nische löschen",
                                  command=lambda: delete_task(columns["Archiv"].get(tk.ANCHOR), "Archiv"))
        delete_button.pack(pady=5)


root = tk.Tk()
root.title("Kanban-Board")

# Fenstergröße und Positionierung anpassen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 2
window_height = screen_height // 2
position_right = int(root.winfo_screenwidth() / 4)
position_down = int(root.winfo_screenheight() / 4)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

kanban_data = load_data()

columns = {}
column_order = ["ToDo", "Done", "Archiv"]
for i, column in enumerate(column_order):
    frame = tk.Frame(root)
    frame.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')

    root.grid_columnconfigure(i, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)  # Damit die Zeilen sich auch dynamisch anpassen

    label = tk.Label(frame, text=column)
    label.pack()

    listbox = tk.Listbox(frame)
    listbox.pack(expand=True, fill='both')
    columns[column] = listbox

    create_buttons(frame, column)

update_board()

root.mainloop()