import sys
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QListView
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

        self.json_db = JSONHandler("../database/notes.json")

        self._setup_ui()
        self._connect_signals()

        self.update_notes_list()

    def _setup_ui(self):
        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(50, 50)

        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("🔎 Search...")

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

    def _connect_signals(self):
        self.add_button.clicked.connect(self.add_button_clicked)
        self.list_view.selectionModel().selectionChanged.connect(self.button_note_clicked)

    def button_note_clicked(self, selected, deselected):
        index = self.list_view.selectionModel().currentIndex()
        if index.isValid():
            note_data = index.data(Qt.UserRole)
            if note_data:
                self._open_rne_note_window(note_data)
            else:
                print("No note selected.")

    def add_button_clicked(self):
        self.add_note_window = AddNoteWindow(self.update_notes_list)
        self.add_note_window.show()

    def _open_rne_note_window(self, note_data):
        self.RnE_note_window = RnENoteWindow(note_data, self.update_notes_list, parent=self)
        self.RnE_note_window.show()

    def update_notes_list(self):
        self.model.clear()
        notes = self.json_db.load_notes()
        if not notes:
            print("No notes found or failed to load notes.")
            return

        for note in notes:
            self._add_note_to_list(note)

    def _add_note_to_list(self, note):
        try:
            title = note.get("title", "Untitled")
            if title:
                item = QStandardItem(title)
                item.setData(note, Qt.UserRole)
                self.model.appendRow(item)
            else:
                print(f"Note missing title or title is empty: {note}")
        except KeyError as e:
            print(f"Error adding note to list: {e}")

    def load_styles(self):
        try:
            with open("../styles/main_window_styles.qss", "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
