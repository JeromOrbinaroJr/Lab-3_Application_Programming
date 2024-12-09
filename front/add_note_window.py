import sys
import uuid

from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLineEdit, QWidget, QPushButton
from back.note import Note
from database import JSONHandler

class AddNoteWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Note")
        self.resize(1200, 700)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.title_line = QLineEdit()
        self.title_line.setPlaceholderText("Enter note title...")

        self.content_line = QLineEdit()
        self.content_line.setPlaceholderText("Enter note content...")

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_button_clicked())

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.addWidget(self.title_line)
        layout.addWidget(self.content_line)
        layout.addWidget(self.add_button)

        central_widget.setLayout(layout)

    def add_button_clicked(self):
        note_id = str(uuid.uuid4())
        category = "General"

        #json_db = JSONHandler("../database/notes.json")
        new_note = Note(id=note_id, title=self.title_line.text(), content=self.content_line.toPlainText(),
                        category=category)
        #json_db.create(new_note)

        self.note_created.emit()
        self.close()

if __name__ == "__main__":
    app =  QApplication(sys.argv)

    window = AddNoteWindow()
    window.show()

    sys.exit(app.exec())