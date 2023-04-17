from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QTableWidget, QTableWidgetItem
import requests
import json


class ClientApp(QMainWindow):
    def __init__(self):
        super(ClientApp, self).__init__()

        self.setWindowTitle('Database')
        self.setGeometry(200, 200, 800, 600)

        # Создание главного виджета
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Создание вертикального контейнера
        layout = QVBoxLayout()

        # Создание метки и поля ввода для имени
        self.name_label = QLabel('Name:')
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # Создание метки и поля ввода для возраста
        self.age_label = QLabel('Age:')
        self.age_input = QLineEdit()
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)

        # Создание метки и поля ввода для адреса
        self.address_label = QLabel('Address:')
        self.address_input = QLineEdit()
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_input)

        # Создание кнопок для добавления и удаления записей
        self.add_button = QPushButton('Add Record')
        self.delete_button = QPushButton('Delete Record')
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        # Создание таблицы для отображения данных
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Address'])
        layout.addWidget(self.table)

        # Установка вертикального контейнера в виджет
        main_widget.setLayout(layout)

        # Подключение сигналов и слотов
        self.add_button.clicked.connect(self.add_record)
        self.delete_button.clicked.connect(self.delete_record)

        # Загрузка данных с сервера
        self.load_records()

    def load_records(self):
        response = requests.get('http://127.0.0.1:8000/get_records')
        if response.status_code == 200:
            records = json.loads(response.text)
            self.table.setRowCount(len(records))
            for i, record in enumerate(records):
                self.table.setItem(i, 0, QTableWidgetItem(str(record['id'])))
                self.table.setItem(i, 1, QTableWidgetItem(record['name']))
                self.table.setItem(i, 2, QTableWidgetItem(str(record['age'])))
                self.table.setItem(i, 3, QTableWidgetItem(record['address']))

    def add_record(self):
        name = self.name_input.text()
        age = self.age_input.text()
        address = self.address_input.text()
        if name and age and address:
            data = {
                'name': str(name),
                'age': int(age),
                'address': str(address)
            }
            response = requests.post('http://127.0.0.1:8000/add_record', json=data)
            if response.status_code == 200:
                self.load_records()
                self.name_input.clear()
                self.age_input.clear()
                self.address_input.clear()

    def delete_record(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            record_id = int(self.table.item(selected_row, 0).text())
            data = {'id': record_id}
            response = requests.post('http://127.0.0.1:8000/delete_record', json=data)
            if response.status_code == 200:
                self.load_records()


if __name__ == '__main__':
    app = QApplication([])
    window = ClientApp()
    window.show()
    app.exec_()
