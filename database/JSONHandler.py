import json
from back.note import Note

class NoteNotFound(Exception):
    pass

class CategoryAlreadyExists(Exception):
    pass

class JSONHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"notes": [], "categories": []}

    def save_data(self, data):
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving data to {self.filepath}: {e}")

    def create(self, note: Note):
        note_data = {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "date": note.date.strftime("%I:%M%p on %B %d, %Y"),
            "category": note.category
        }

        data = self.load_data()
        data["notes"].append(note_data)
        self.save_data(data)

    def update_note(self, updated_note: Note):
        data = self.load_data()

        updated = False
        for note in data.get("notes", []):
            if note["id"] == updated_note.id:
                note.update({
                    "title": updated_note.title,
                    "content": updated_note.content,
                    "category": updated_note.category,
                })
                updated = True
                break

        if updated:
            self.save_data(data)
        else:
            raise NoteNotFound(f"Note with ID {updated_note.id} not found.")

    def load_notes(self):
        data = self.load_data()
        return data.get("notes", [])

    def delete_note(self, note_id):
        data = self.load_data()
        notes = data.get("notes", [])

        data["notes"] = [note for note in notes if note["id"] != note_id]

        self.save_data(data)
        return True

    def get_categories(self):
        data = self.load_data()
        return data.get("categories", [])

    def add_category(self, category):
        data = self.load_data()
        categories = data.get("categories", [])
        if category not in categories:
            categories.append(category)
            data["categories"] = categories
            self.save_data(data)
        else:
            raise CategoryAlreadyExists(f"Category '{category}' already exists.")