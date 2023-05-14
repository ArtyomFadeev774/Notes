from PyQt5 import QtGui, QtWidgets
import json

app = QtWidgets.QApplication([])

class MainWindow(QtWidgets.QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.resize(width, height)
        self.setWindowTitle('Заметки')
        self.setWindowIcon(QtGui.QIcon(r'C:\Program Files\notesFiles\main.png'))
        self.globalHline = QtWidgets.QHBoxLayout() #главная горизонтальная линия
        self.globalVline1 = QtWidgets.QVBoxLayout()
        self.globalVline2 = QtWidgets.QVBoxLayout()
        self.searchLineLayout = QtWidgets.QHBoxLayout()
        #виджеты
        self.notesText = QtWidgets.QTextEdit()
        self.titleTextNotes = QtWidgets.QLabel('Список заметок:')
        self.listNotes = QtWidgets.QListWidget()
        self.createNoteButton = QtWidgets.QPushButton('Создать заметку')
        self.deleteNoteButton = QtWidgets.QPushButton('Удалить заметку')
        self.saveNoteButton = QtWidgets.QPushButton('Сохранить заметку')
        self.tagsTitle = QtWidgets.QLabel('Список тегов:')
        self.listTags = QtWidgets.QListWidget()
        self.searchLine = QtWidgets.QLineEdit()
        self.searchLine.setPlaceholderText('Введите тег...')
        self.clearButton = QtWidgets.QPushButton(icon=QtGui.QIcon(r'C:\Program Files\notesFiles\iconDel.png'))
        self.addTagButton = QtWidgets.QPushButton('Добавить к заметке')
        self.delTagButton = QtWidgets.QPushButton('Открепить от заметки')
        self.searchNoteButton = QtWidgets.QPushButton('Искать заметки по тегу')
        #заркепление на лайаутах
        self.globalVline1.addWidget(self.notesText)
        self.globalVline2.addWidget(self.titleTextNotes)
        self.globalVline2.addWidget(self.listNotes)
        self.globalVline2.addWidget(self.createNoteButton)
        self.globalVline2.addWidget(self.deleteNoteButton)
        self.globalVline2.addWidget(self.saveNoteButton)
        self.globalVline2.addWidget(self.tagsTitle)
        self.globalVline2.addWidget(self.listTags)
        self.searchLineLayout.addWidget(self.searchLine, 90)
        self.searchLineLayout.addWidget(self.clearButton, 10)
        self.globalVline2.addLayout(self.searchLineLayout)
        self.globalVline2.addWidget(self.addTagButton)
        self.globalVline2.addWidget(self.delTagButton)
        self.globalVline2.addWidget(self.searchNoteButton)
        self.globalHline.addLayout(self.globalVline1)
        self.globalHline.addLayout(self.globalVline2)
        self.setLayout(self.globalHline)

window = MainWindow(1000, 700)
window.show()

notes = {}

def dump():
    try:
        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file)
    except FileNotFoundError as e:
        show_message('Ошибка', e, r'C:\Program Files\notesFiles\warning.png')

def load():
    global notes
    try:
        with open('notes.json', 'r', encoding='utf-8') as file:
            notes = json.load(file)
    except FileNotFoundError as e:
        show_message('Ошибка', e, r'C:\Program Files\notesFiles\warning.png')

load()
window.listNotes.addItems(notes.keys())

def show_notes():
    name = window.listNotes.selectedItems()[0].text()
    note_text = notes[name]['text']
    note_tags = notes[name]['tags']
    window.notesText.setText(note_text)
    window.listTags.clear()
    window.listTags.addItems(note_tags)

def add_note():
    note_name, result = QtWidgets.QInputDialog.getText(window, 'Добавить заметку', 'Название:')
    if result and note_name != '':
        notes[note_name] = {
            'text': '',
            'tags': []
        }
        dump()
        window.listNotes.clear()
        window.listNotes.addItems(notes.keys())

def show_message(title:str, text:str, icon=r'C:\Program Files\notesFiles\main.png') -> None:
    message = QtWidgets.QMessageBox(window)
    message.setWindowTitle(str(title))
    message.setWindowIcon(QtGui.QIcon(icon))
    message.setText(str(text))
    message.show()
    message.exec_()

def delete_note():
    if len(window.listNotes.selectedItems()) != 0:
        try:
            del notes[window.listNotes.selectedItems()[0].text()]
            dump()
            window.listNotes.clear()
            window.listNotes.addItems(notes.keys())
            show_message('Уведомление', 'Заметка удалена.', r'C:\Program Files\notesFiles\sucsess.png')
        except FileNotFoundError as e:
            show_message('Ошибка', e, r'C:\Program Files\notesFiles\warning.png')
    else:
        show_message('Предупреждение', 'Выберите заметку для удаления.', r'C:\Program Files\notesFiles\warning.png')

def save_note():
    if len(window.listNotes.selectedItems()) != 0:
        key = window.listNotes.selectedItems()[0].text()
        text = window.notesText.toPlainText() #возвращает текст заметки
        notes[key]['text'] = text
        dump()
        show_message('Уведомление', 'Данные сохранены.', r'C:\Program Files\notesFiles\sucsess.png')
    else:
        show_message('Предупреждение', 'Выберите заметку для сохранения.', r'C:\Program Files\notesFiles\warning.png')

def add_tag():
    if len(window.listNotes.selectedItems()) != 0:
        if window.searchLine.text() != '' and window.searchLine.text().isspace() == False:
            key = window.listNotes.selectedItems()[0].text()
            if window.searchLine.text() not in notes[key]['tags']:
                notes[key]['tags'].append(window.searchLine.text())
                dump()
                window.listTags.clear()
                window.listTags.addItems(notes[key]['tags'])
            else:
                show_message('Ошибка', 'Данный тег уже присутствует.', r'C:\Program Files\notesFiles\warning.png')
            window.searchLine.clear()
        else:
            show_message('Ошибка', 'Введён пустой текст.', r'C:\Program Files\notesFiles\warning.png')
    else:
        show_message('Предупреждение', 'Выберите заметку для добавления тега.', r'C:\Program Files\notesFiles\warning.png')

def delete_tag():
    if len(window.listTags.selectedItems()) != 0:
        key = window.listNotes.selectedItems()[0].text()
        notes[key]['tags'].remove(window.listTags.selectedItems()[0].text())
        window.listTags.clear()
        dump()
        window.listTags.addItems(notes[key]['tags'])
    else:
        show_message('Предупреждение', 'Выберите тег для удаления.', r'C:\Program Files\notesFiles\warning.png')

def search_tag():
    if window.searchLine.text() != '':
        if window.searchLine.text().isspace() == False:
            l = []
            for element in notes:
                if window.searchLine.text() in  notes[element]['tags']:
                    l.append(element)
            window.listNotes.clear()
            window.listNotes.addItems(l)
            if len(l) == 0:
                show_message('Уведомление', 'Заметок с таким тегом не найдено.', r'C:\Program Files\notesFiles\warning.png')
    else:
        window.listNotes.clear()
        window.listNotes.addItems(notes)

def clearSearchLine():
    window.searchLine.clear()
    window.listNotes.clear()
    window.listNotes.addItems(notes)
        
window.listNotes.itemClicked.connect(show_notes)
window.createNoteButton.clicked.connect(add_note)
window.deleteNoteButton.clicked.connect(delete_note)
window.saveNoteButton.clicked.connect(save_note)
window.addTagButton.clicked.connect(add_tag)
window.delTagButton.clicked.connect(delete_tag)
window.searchNoteButton.clicked.connect(search_tag)
window.clearButton.clicked.connect(clearSearchLine)

app.exec_()