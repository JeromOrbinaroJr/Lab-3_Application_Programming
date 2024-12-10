import sys
import uuid
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLineEdit, QWidget, QPushButton, QLabel, QFormLayout
from back.note import Note
from database.JSONHandler import JSONHandler


class AddNoteWindow(QMainWindow):
    def __init__(self, update_callback):
        super().__init__()

        self.setWindowTitle("Add Note")
        self.resize(900, 500)

        self.update_callback = update_callback
        self.json_db = JSONHandler("../database/notes.json")

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.title_line = QLineEdit()
        self.title_line.setPlaceholderText("Enter note title...")

        self.content_line = QLineEdit()
        self.content_line.setPlaceholderText("Enter note content...")

        self.add_button = QPushButton("Add")
        self.add_button.setFixedHeight(40)
        self.add_button.clicked.connect(self.add_button_clicked)

        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Title:"), self.title_line)
        form_layout.addRow(QLabel("Content:"), self.content_line)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.addLayout(form_layout)
        layout.addWidget(self.add_button)

    def add_button_clicked(self):
        note_id = str(uuid.uuid4())
        category = "General"

        new_note = Note(
            id=note_id,
            title=self.title_line.text(),
            content=self.content_line.text(),
            category=category,
        )

        self.json_db.create(new_note)

        self.update_callback()

        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AddNoteWindow(lambda: print("Notes list updated"))
    window.show()

    sys.exit(app.exec())
