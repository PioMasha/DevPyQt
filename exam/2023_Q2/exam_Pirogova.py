import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget, QDateTimeEdit
from PySide6.QtCore import QDateTime


class Note:
    def __init__(self, title, description, deadline):
        """Инициализирую создание атрибутов объекта этого класса"""
        self.title = title
        self.description = description
        self.deadline = deadline

    def to_dict(self):
        """Преобразую в словарь"""
        return {
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline.toString("yyyy-MM-dd HH:mm:ss")
        }


class NotesApp(QMainWindow):
    def __init__(self):
        """Инициализирую главное окно приложения и его основные компоненты"""
        super().__init__()

        self.setWindowTitle("Заметки")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.notes = []
        self.current_note_index = -1

        self.init_ui()
        self.load_notes_from_json()

    def init_ui(self):
        """Инициализирую графический интерфейс, размещение виджетов, устанавливаю обработчик"""
        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.description_input = QTextEdit()
        self.deadline_input = QDateTimeEdit()

        add_button = QPushButton("Добавить заметку")
        edit_button = QPushButton("Редактировать заметку")
        delete_button = QPushButton("Удалить заметку")

        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.select_note)

        layout.addWidget(QLabel("Заголовок:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Описание:"))
        layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Дедлайн:"))
        layout.addWidget(self.deadline_input)
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.addWidget(self.notes_list)

        add_button.clicked.connect(self.add_note)
        edit_button.clicked.connect(self.edit_note)
        delete_button.clicked.connect(self.delete_note)

        self.central_widget.setLayout(layout)

    def add_note(self):
        """Добавление новой заметки, сохранение её"""
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        deadline = self.deadline_input.dateTime()

        if title:
            new_note = Note(title, description, deadline)
            self.notes.append(new_note)
            self.save_notes_to_json()
            self.update_notes_list()

    def edit_note(self):
        """Редактирование существующей заметки"""
        if self.current_note_index != -1:
            title = self.title_input.text()
            description = self.description_input.toPlainText()
            deadline = self.deadline_input.dateTime()

            if title:
                edited_note = Note(title, description, deadline)
                self.notes[self.current_note_index] = edited_note
                self.save_notes_to_json()
                self.update_notes_list()

    def delete_note(self):
        """Удаление существующей заметки"""
        if self.current_note_index != -1:
            del self.notes[self.current_note_index]
            self.save_notes_to_json()
            self.update_notes_list()

    def select_note(self, item):
        """Отображение выбранной заметки"""
        self.current_note_index = self.notes_list.currentRow()
        note = self.notes[self.current_note_index]
        self.title_input.setText(note.title)
        self.description_input.setPlainText(note.description)
        self.deadline_input.setDateTime(note.deadline)

    def update_notes_list(self):
        """Обновление списка заметок"""
        self.notes_list.clear()
        for note in self.notes:
            self.notes_list.addItem(note.title)

    def save_notes_to_json(self):
        """Сохранение списка заметок в JSON в файле"""
        with open('notes.json', 'w') as file:
            notes_data = [note.to_dict() for note in self.notes]
            json.dump(notes_data, file)

    def load_notes_from_json(self):
        """Загрузка списка заметок из файла в JSON"""
        try:
            with open('notes.json', 'r') as file:
                data = json.load(file)
                self.notes = []
                for note in data:
                    if all(key in note for key in ('title', 'description', 'deadline')):
                        deadline = QDateTime.fromString(note['deadline'], "yyyy-MM-dd HH:mm:ss")
                        new_note = Note(note['title'], note['description'], deadline)
                        self.notes.append(new_note)
                self.update_notes_list()
        except FileNotFoundError:
            initial_notes = [
                {
                    'title': 'Первая заметка',
                    'description': 'Описание первой заметки',
                    'deadline': '2023-12-31 23:59:59'
                },
                {
                    'title': 'Вторая заметка',
                    'description': 'Описание второй заметки',
                    'deadline': '2023-12-25 18:00:00'
                }
            ]
            self.notes = [
                Note(note['title'], note['description'], QDateTime.fromString(note['deadline'], "yyyy-MM-dd HH:mm:ss"))
                for note in initial_notes]
            self.save_notes_to_json()
            self.update_notes_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notes_app = NotesApp()
    notes_app.show()
    sys.exit(app.exec_())
