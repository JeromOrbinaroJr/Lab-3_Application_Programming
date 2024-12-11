import sys
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QListView
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt
from front.add_note_window import AddNoteWindow
from database.JSONHandler import JSONHandler
from front.RnE_note_window import RnENoteWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NoTextNerv")
        self.resize(1100, 600)

        self.load_styles()

        try:
            self.json_db = JSONHandler("../database/notes.json")
        except Exception as e:
            print(f"Error initializing database handler: {e}")
            self.json_db = None

        self.setup_ui()
        self.connect_signals()

        if self.json_db:
            self.update_notes_list()

    def setup_ui(self):
        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(50, 50)

        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("\U0001F50E Search...")

        self.list_view = QListView()
        self.model = QStandardItemModel(self.list_view)
        self.list_view.setModel(self.model)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.search_line, stretch=1)
        top_layout.addWidget(self.add_button)

        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.list_view)

    def connect_signals(self):
        self.add_button.clicked.connect(self.add_button_clicked)
        self.search_line.textChanged.connect(self.search_notes)
        self.list_view.selectionModel().selectionChanged.connect(self.button_note_clicked)

    def button_note_clicked(self, selected, deselected):
        index = self.list_view.selectionModel().currentIndex()
        if index.isValid():
            note_data = index.data(Qt.UserRole)
            if note_data:
                self.open_rne_note_window(note_data)

    def add_button_clicked(self):
        self.add_note_window = AddNoteWindow(self.update_notes_list)
        self.add_note_window.show()

    def open_rne_note_window(self, note_data):
        try:
            self.rne_note_window = RnENoteWindow(note_data, self.update_notes_list, parent=self)
            self.rne_note_window.show()
        except Exception as e:
            print(f"Error opening RnE note window: {e}")

    def update_notes_list(self):
        if self.json_db:
            self.model.clear()
            try:
                notes = self.json_db.load_notes()
                if not notes:
                    return
                for note in notes:
                    self.add_note_to_list(note)
            except Exception as e:
                print(f"Error loading notes: {e}")

    def add_note_to_list(self, note):
        try:
            title = note.get("title", "Untitled")
            category = note.get("category", "Uncategorized")
            display_text = f"{title} ({category})"

            if title:
                item = QStandardItem(display_text)
                item.setData(note, Qt.UserRole)
                self.model.appendRow(item)
            else:
                print(f"Note missing title or title is empty: {note}")
        except KeyError as e:
            print(f"Error adding note to list: {e}")
        except Exception as e:
            print(f"Unexpected error adding note to list: {e}")

    def search_notes(self):
        try:
            search_text = self.search_line.text().lower()
            if self.json_db:
                notes = self.json_db.load_notes()
                filtered_notes = [note for note in notes if search_text in note.get("title", "").lower()]
                self.model.clear()
                for note in filtered_notes:
                    self.add_note_to_list(note)
        except Exception as e:
            print(f"Error during search: {e}")

    def load_styles(self):
        try:
            with open("../styles/main_window_styles.qss", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError as e:
            print(f"Stylesheet file not found: {e}")
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        sys.exit(app.exec())
    except Exception as e:
        print(f"Unexpected error during application execution: {e}")
        sys.exit(1)
