import sys
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton
from database.JSONHandler import JSONHandler

class RnENoteWindow(QMainWindow):
    def __init__(self, note_data=None):
        super().__init__()
        self.setWindowTitle("Read&Edit Note")
        self.resize(900, 500)

        self.note_data = note_data

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        form_layout = QFormLayout()

        self.title_edit = QLineEdit(self.note_data.get("title", ""))
        self.title_edit.setPlaceholderText("Enter the title of your note...")
        form_layout.addRow(QLabel("Title:"), self.title_edit)

        self.content_edit = QLineEdit(self.note_data.get("content", ""))
        self.content_edit.setPlaceholderText("Enter the content of your note...")
        form_layout.addRow(QLabel("Content:"), self.content_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_note)

    def save_note(self):
        self.note_data["title"] = self.title_edit.text()
        self.note_data["content"] = self.content_edit.text()

        json_db = JSONHandler("../database/notes.json")
        json_db.update_note(self.note_data)

        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = RnENoteWindow()
    window.show()

    sys.exit(app.exec())