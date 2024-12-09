import json
from back.note import Note

def NoteNotFound(Exception):
    pass

class JSONHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def create(self, note: Note):
        note_data = {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "date": note.date.strftime("%I:%M%p on %B %d, %Y"),
            "category": note.category
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"notes": []}

        data["notes"].append(note_data)

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)


    def update_note(self, updated_note: Note):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for note in data.get("notes", []):
                if note["id"] == updated_note["id"]:
                    note.update(updated_note)
                    break

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error updating note: {e}")

    def load_notes(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                return data.get("notes", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading notes: {e}")
            return []

    def delete_note(self, note_id):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            data["notes"] = [note for note in data.get("notes", []) if note["id"] != note_id]

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True

        except (FileNotFoundError, json.JSONDecodeError):
            return False