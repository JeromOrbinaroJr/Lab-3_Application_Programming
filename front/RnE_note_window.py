import sys
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QComboBox, QTextEdit, QMessageBox
from PySide6.QtCore import QDateTime
from back.note import Note
from database.JSONHandler import JSONHandler

class RnENoteWindow(QMainWindow):
    def __init__(self, note_data, update_callback, parent=None):
        super().__init__(parent)
        self.note_data = note_data
        self.update_callback = update_callback

        try:
            self.json_db = JSONHandler("../database/notes.json")
        except Exception as e:
            print(f"Error initializing database handler: {e}")
            self.json_db = None

        self.setWindowTitle(f"Read & Edit: {self.note_data.get('title', 'Untitled')}")
        self.resize(900, 500)

        self.setup_ui()

    def setup_ui(self):
        try:
            self.load_styles()
        except Exception as e:
            self.show_error_message(f"Error loading styles: {e}")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        form_layout = QFormLayout()

        self.title_edit = QLineEdit(self.note_data.get("title", ""))
        self.title_edit.setPlaceholderText("Enter the title of your note...")
        form_layout.addRow(QLabel("Title:"), self.title_edit)

        self.content_edit = QTextEdit(self.note_data.get("content", ""))
        self.content_edit.setPlaceholderText("Enter the content of your note...")
        self.content_edit.setFixedHeight(150)
        form_layout.addRow(QLabel("Content:"), self.content_edit)

        self.category_combobox = QComboBox()
        self.load_categories()
        self.category_combobox.setCurrentText(self.note_data.get("category", "General"))
        form_layout.addRow(QLabel("Category:"), self.category_combobox)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_note)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.confirm_delete_note)

        self.date_label = QLabel(self)
        self.update_time_label()

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.date_label)

    def load_categories(self):
        try:
            categories = self.json_db.get_categories()
            if categories is None:
                raise ValueError("Categories not found or database is empty.")
            self.category_combobox.addItems(categories)
        except Exception as e:
            print(f"Error loading categories: {e}")
            self.category_combobox.addItem("General")

    def save_note(self):
        try:
            title = self.title_edit.text().strip()
            content = self.content_edit.toPlainText().strip()

            if not title or not content:
                print("Title and content cannot be empty!")
                return

            self.note_data["title"] = title
            self.note_data["content"] = content
            self.note_data["category"] = self.category_combobox.currentText()
            self.note_data["date"] = QDateTime.currentDateTime().toString()

            updated_note = Note(
                id=self.note_data["id"],
                title=self.note_data["title"],
                content=self.note_data["content"],
                category=self.note_data["category"],
                date=self.note_data["date"],
            )

            self.json_db.update_note(updated_note)
            self.update_callback()
            self.show_message("Success", "Note updated successfully.", QMessageBox.Information)
            self.close()

        except ValueError as ve:
            self.show_message("Error", f"Validation error: {ve}", QMessageBox.Warning)
        except Exception as e:
            self.show_message("Error", f"Error updating note: {e}", QMessageBox.Warning)

    def confirm_delete_note(self):
        reply = QMessageBox.question(self, "Confirm Deletion",
                                     "Are you sure you want to delete this note?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.delete_note()

    def delete_note(self):
        try:
            if self.json_db.delete_note(self.note_data["id"]):
                self.update_callback()
                self.show_message("Success", "Note deleted successfully.", QMessageBox.Information)
                self.close()
            else:
                self.show_message("Error", "Error deleting note.", QMessageBox.Warning)
        except Exception as e:
            self.show_message("Error", f"Error deleting note: {e}", QMessageBox.Warning)

    def update_time_label(self):
        try:
            note_datetime_str = self.note_data.get("date", "Unknown")
            self.date_label.setText(f"Date: {note_datetime_str}")
        except Exception as e:
            print(f"Error updating time label: {e}")

    def load_styles(self):
        try:
            with open("../styles/RnE_window_styles.qss", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError as fnf_error:
            print(f"Stylesheet file not found: {fnf_error}")
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    def show_message(self, title, text, icon):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setIcon(icon)
        msg_box.exec()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        test_note = {
            "id": "1",
            "title": "Test Note",
            "content": "Test content.",
            "category": "General",
            "date": "2024-12-10",
        }

        window = RnENoteWindow(
            note_data=test_note,
            update_callback=lambda: print("Notes list updated")
        )
        window.show()

        sys.exit(app.exec())

    except Exception as e:
        print(f"Error running the application: {e}")
        sys.exit(1)
