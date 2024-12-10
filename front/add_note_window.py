import sys
import uuid
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLineEdit, QTextEdit, QWidget, QPushButton, QLabel, \
    QFormLayout, QInputDialog, QComboBox
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
        self.load_styles()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.title_line = QLineEdit()
        self.title_line.setPlaceholderText("Enter note title...")

        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Enter note content...")
        self.content_edit.setFixedHeight(150)

        self.category_combobox = QComboBox()
        self.category_combobox.addItem("General")
        self.load_categories()

        self.create_category_button = QPushButton("Create New Category")
        self.create_category_button.clicked.connect(self.create_category)

        self.add_button = QPushButton("Add")
        self.add_button.setFixedHeight(40)
        self.add_button.clicked.connect(self.add_button_clicked)

        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Title:"), self.title_line)
        form_layout.addRow(QLabel("Content:"), self.content_edit)
        form_layout.addRow(QLabel("Category:"), self.category_combobox)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.addLayout(form_layout)
        layout.addWidget(self.create_category_button)
        layout.addWidget(self.add_button)

    def load_categories(self):
        categories = self.json_db.get_categories()
        self.category_combobox.addItems(categories)

    def create_category(self):
        new_category, ok = QInputDialog.getText(self, "New Category", "Enter category name:")
        if ok and new_category:
            self.json_db.add_category(new_category)
            self.category_combobox.addItem(new_category)

    def add_button_clicked(self):
        note_id = str(uuid.uuid4())
        category = self.category_combobox.currentText()

        new_note = Note(
            id=note_id,
            title=self.title_line.text(),
            content=self.content_edit.toPlainText(),
            category=category,
        )

        self.json_db.create(new_note)

        self.update_callback()
        self.close()

    def load_styles(self):
        try:
            with open("../styles/add_note_window_style.qss", "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AddNoteWindow(lambda: print("Notes list updated"))
    window.show()

    sys.exit(app.exec())
