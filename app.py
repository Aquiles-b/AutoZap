from PySide6 import QtWidgets, QtCore, QtGui
import json
import os

class App(QtWidgets.QApplication):
    def __init__(self):
        super().__init__()
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("AutoZap")
        self.contacts_data = self._load_contacts_data()
        self._create_layout()
        self._basic_ui_widgets()
        self._update_contacts()
        self._updateMessages()
        self._create_add_contact_window()
        self.window.setLayout(self.main_layout)
        self.window.show()
        self.exec()

    def _load_contacts_data(self):
        if os.path.exists("contacts_data.json"):
            with open("contacts_data.json", "r") as file:
                return json.load(file)
        else:
            return []

    def _save_contacts_data(self):
        with open("contacts_data.json", "w") as file:
            json.dump(self.contacts_data, file)

    def _create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.menu_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.menu_layout)

        self.operation_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.operation_layout)

        self.contacts = QtWidgets.QListWidget()
        self.messages = QtWidgets.QListWidget()
        self.operation_layout.addWidget(self.contacts)
        self.operation_layout.addWidget(self.messages)

    def _basic_ui_widgets(self):
        self.add_contact_button = QtWidgets.QPushButton("Add Contact")
        self.add_contact_button.clicked.connect(self.add_contact)
        self.menu_layout.addWidget(self.add_contact_button)

        self.delete_contact_button = QtWidgets.QPushButton("Delete Contact")
        self.delete_contact_button.clicked.connect(self.deleteContact)
        self.menu_layout.addWidget(self.delete_contact_button)

        self.refresh_button = QtWidgets.QPushButton("Refresh")
        # self.refresh_button.clicked.connect(self.refresh)
        self.menu_layout.addWidget(self.refresh_button)

        self.message_layout = QtWidgets.QVBoxLayout()
        self.operation_layout.addLayout(self.message_layout)

    def _update_contacts(self):
        self.contacts.clear()
        for contact in self.contacts_data:
            # Draw a rectangle with the contact's name and number
            item = QtWidgets.QListWidgetItem(contact["name"] + " - " + contact["number"])
            self.contacts.addItem(item)

    def _updateMessages(self):
        pass

    def _create_add_contact_window(self):
        self.add_contact_window = QtWidgets.QWidget()
        self.add_contact_window.setWindowTitle("Add Contact")
        self.add_contact_window.resize(300, 100)
        self.add_contact_window.setLayout(QtWidgets.QVBoxLayout())

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.add_contact_window.layout().addWidget(self.name_input)

        self.number_input = QtWidgets.QLineEdit()
        self.number_input.setPlaceholderText("Number")
        self.add_contact_window.layout().addWidget(self.number_input)

        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_contact)
        self.add_contact_window.layout().addWidget(self.submit_button)

    def add_contact(self):
        self.add_contact_window.show()

    def deleteContact(self):
        row = self.contacts.currentRow()
        if row >= 0:
            del self.contacts_data[row]
            self._save_contacts_data()
            self._update_contacts()

    def submit_contact(self):
        name = self.name_input.text()
        number = self.number_input.text()
        self.contacts_data.append({
            "name": name,
            "number": number
        })
        self._save_contacts_data()
        self._update_contacts()
        self.add_contact_window.close()

app = App()
