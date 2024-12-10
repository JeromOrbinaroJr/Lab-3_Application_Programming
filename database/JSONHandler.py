import json
from back.note import Note

class NoteNotFound(Exception):
    pass

class JSONHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def _load_data(self):
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"notes": [], "categories": []}

    def _save_data(self, data):
        try:
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
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

        data = self._load_data()
        data["notes"].append(note_data)
        self._save_data(data)

    def update_note(self, updated_note: Note):
        data = self._load_data()

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
            self._save_data(data)
        else:
            raise NoteNotFound(f"Note with ID {updated_note.id} not found.")

    def load_notes(self):
        data = self._load_data()
        return data.get("notes", [])

    def delete_note(self, note_id):
        data = self._load_data()
        notes = data.get("notes", [])

        data["notes"] = [note for note in notes if note["id"] != note_id]

        self._save_data(data)
        return True

    def get_categories(self):
        data = self._load_data()
        return data.get("categories", [])

    def add_category(self, category):
        data = self._load_data()
        categories = data.get("categories", [])
        if category not in categories:
            categories.append(category)
            data["categories"] = categories
            self._save_data(data)

