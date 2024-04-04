from PyQt5.QtCore import Qt
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit, QListWidget, \
    QHBoxLayout, QLineEdit, QInputDialog

#  главное окно
app = QApplication([])
main = QWidget()
main.setWindowTitle('_умные заметки_ ')
main.resize(900, 600)

#   левая колонка
text_field = QTextEdit()

#  правая колонка
#  блок заметок
notes_label = QLabel('Список заметок')
list_notes = QListWidget()
button_note_add = QPushButton('_создать заметку_')
button_note_del = QPushButton('_удалить заметку_')
button_note_save = QPushButton('_сохранить заметку_')

#  блок тегов
tags_label = QLabel('Список тегов')
list_tags = QListWidget()
tag_field = QLineEdit()
tag_field.setPlaceholderText('Введите тег...')
button_tag_add = QPushButton('_добавить к заметке_')
button_tag_del = QPushButton('_открепить от заметки_')
button_tag_search = QPushButton('_искать заметку по тегу_')

#  лэяуты
main_line = QHBoxLayout()

#  левая колонка
col_line1 = QVBoxLayout()
col_line1.addWidget(text_field)

#  правая колонка
col_line2 = QVBoxLayout()

#  блок заметок
col_line2.addWidget(notes_label)
col_line2.addWidget(list_notes)
row_line1 = QHBoxLayout()
row_line1.addWidget(button_note_add)
row_line1.addWidget(button_note_del)
col_line2.addWidget(button_note_save)
col_line2.addLayout(row_line1)
col_line2.addStretch(1)

#  блок тегов
col_line2.addWidget(tags_label)
col_line2.addWidget(list_tags)
col_line2.addWidget(tag_field)
row_line2 = QHBoxLayout()
row_line2.addWidget(button_tag_add)
row_line2.addWidget(button_tag_del)
col_line2.addLayout(row_line2)
col_line2.addWidget(button_tag_search)
col_line2.addStretch(1)

main_line.addLayout(col_line1, stretch=20)
main_line.addStretch(1)
main_line.addLayout(col_line2, stretch=4)
main_line.addStretch(1)
main.setLayout(main_line)


def show_note():
    name = list_notes.selectedItems()[0].text()
    text_field.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['теги'])


def add_note():
    note_name, result = QInputDialog.getText(
        main, 'название новой заметки', 'название заметки'
    )
    if note_name != '':
        notes[note_name] = {'текст': '', 'теги': []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])


def save_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        notes[name]['текст'] = text_field.toPlainText()
        with open('zametky.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)


def del_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        del notes[name]

        with open('zametky.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

        text_field.clear()
        tag_field.clear()
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes)

def add_tag():
    if tag_field.text() != '':
        if list_notes.selectedItems():
            tag = tag_field.text()
            note_name = list_notes.selectedItems()[0].text()
            tag_field.clear()
            if tag not in notes[note_name]['теги']:
                notes[note_name]['теги'].append(tag)

                with open('zametky.json', 'w') as file:
                    json.dump(notes, file, sort_keys=True)
                list_tags.addItem(tag)

def del_tag():
    if list_tags.selectedItems():
        tag = list_tags.selectedItems()[0].text()
        note_name = list_notes.selectedItems()[0].text()
        notes[note_name]['теги'].remove(tag)

        with open('zametky.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

        list_tags.clear()
        list_tags.addItems(notes[note_name]['теги'])

def find_tag():
    tag = tag_field.text()
    if button_tag_search.text() == '_искать заметку по тегу_':
        notes_filter = {}
        for note_name in notes:
            if tag in notes[note_name]['теги']:
                notes_filter[note_name] = notes[note_name]
        button_tag_search.setText('_сбросить поиск_')
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes_filter)
    elif button_tag_search.text() == '_сбросить поиск_':
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('_искать заметку по тегу_')


button_tag_search.clicked.connect(find_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_add.clicked.connect(add_tag)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_note_add.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
with open('zametky.json', 'r', encoding='utf8') as file:
    notes = json.load(file)

list_notes.addItems(notes)
main.show()
app.exec_()
