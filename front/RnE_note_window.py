import sys
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QLabel, \
    QPushButton, QComboBox, QTextEdit
from PySide6.QtCore import QDateTime
from back.note import Note
from database.JSONHandler import JSONHandler


class RnENoteWindow(QMainWindow):
    def __init__(self, note_data, update_callback, parent=None):
        super().__init__(parent)
        self.note_data = note_data
        self.update_callback = update_callback
        self.json_db = JSONHandler("../database/notes.json")

        self.setWindowTitle(f"Read&Edit {self.note_data.get('title', 'Untitled')}")
        self.resize(900, 500)

        self._setup_ui()

    def _setup_ui(self):
        self.load_styles()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        form_layout = QFormLayout()

        self.title_edit = QLineEdit(self.note_data.get("title", ""))
        self.title_edit.setPlaceholderText("Enter the title of your note...")
        form_layout.addRow(QLabel("Title:"), self.title_edit)

        self.content_edit = QTextEdit(self.note_data.get("content", ""))
        self.content_edit.setPlaceholderText("Enter the content of your note...")
        self.content_edit.setFixedHeight(150)  # Set fixed height for content input
        form_layout.addRow(QLabel("Content:"), self.content_edit)

        self.category_combobox = QComboBox()
        self.load_categories()  # Load all categories
        self.category_combobox.setCurrentText(self.note_data.get("category", "General"))
        form_layout.addRow(QLabel("Category:"), self.category_combobox)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_note)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_note)

        self.date_label = QLabel(self)
        self.update_time_label()

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.date_label)

    def load_categories(self):
        categories = self.json_db.get_categories()
        self.category_combobox.addItems(categories)

    def save_note(self):
        self.note_data["title"] = self.title_edit.text()
        self.note_data["content"] = self.content_edit.toPlainText()
        self.note_data["category"] = self.category_combobox.currentText()

        current_datetime = QDateTime.currentDateTime().toString()

        updated_note = Note(
            id=self.note_data["id"],
            title=self.note_data["title"],
            content=self.note_data["content"],
            category=self.note_data["category"],
            date=current_datetime
        )

        self.json_db.update_note(updated_note)
        self.close()
        self.update_callback()

    def delete_note(self):
        if self.json_db.delete_note(self.note_data["id"]):
            print("Note deleted successfully.")
            self.update_callback()
            self.close()
        else:
            print("Error deleting the note.")

    def update_time_label(self):
        note_datetime_str = self.note_data.get("date", "")
        self.date_label.setText(f"Date: {note_datetime_str}")

    def load_styles(self):
        try:
            with open("../styles/RnE_window_styles.qss", "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = RnENoteWindow(
        note_data={"id": "1", "title": "Test", "content": "Test content", "date": "2024-12-10"},
        update_callback=lambda: print("Notes list updated")
    )
    window.show()

    sys.exit(app.exec())
