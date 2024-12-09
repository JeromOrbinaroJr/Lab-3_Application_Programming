import sys
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QListView, QListWidget
from front.add_note_window import AddNoteWindow
from database.JSONHandler import JSONHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NoTextNerv")
        self.resize(1300, 800)

        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(50, 50)
        self.add_button.clicked.connect(self.add_button_clicked)

        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("🔎 Search...")

        self.json_db = JSONHandler("../database/notes.json")

        self.list_notes = QListWidget()
        self.update_notes_list()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.search_line, stretch=1)
        top_layout.addWidget(self.add_button)

        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(top_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.list_notes)

    def add_button_clicked(self):
        self.add_note_window = AddNoteWindow()
        self.add_note_window.show()
        self.add_note_window.closeEvent = self.update_notes_list_event

    def update_notes_list_event(self, event):
        self.update_notes_list()

    def update_notes_list(self):
        self.list_notes.clear()
        self.list_notes.addItems(self.json_db.load_notes())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

