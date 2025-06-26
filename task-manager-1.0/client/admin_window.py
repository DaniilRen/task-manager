#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel

from library import send_request
from library import showDialog
from user_window import UserWindow


class AdminWindow(QWidget):
	
	def __init__(self):
		super().__init__()
		
		self.setFixedSize(800, 600)
		
		# Set window properties
		self.setWindowTitle("Клиент администратора")
		
		main_layout = QVBoxLayout(self)
		margin = 5
		main_layout.setContentsMargins(margin, margin, margin, margin)

		# Create GUI components
		self.users_list_label = QLabel("Список пользователей:")
		main_layout.addWidget(self.users_list_label)
		
		self.users_list = QComboBox(self)
		self.users_list.currentIndexChanged.connect(self.index_changed)
		main_layout.addWidget(self.users_list)
		
		self.name_label = QLabel("Имя пользователя:")
		main_layout.addWidget(self.name_label)
		
		self.name_line = QLineEdit(self)
		self.name_line.setText('Имя')
		main_layout.addWidget(self.name_line)
		
		self.surname_label = QLabel("Фамилия пользователя:")
		main_layout.addWidget(self.surname_label)
		
		self.surname_line = QLineEdit(self)
		self.surname_line.setText('Фамилия')
		main_layout.addWidget(self.surname_line)
		
		self.thirdname_label = QLabel("Отчество пользователя:")
		main_layout.addWidget(self.thirdname_label)
		
		self.thirdname_line = QLineEdit(self)
		self.thirdname_line.setText('Отчество')
		main_layout.addWidget(self.thirdname_line)
		
		self.id_label = QLabel("Идентификатор пользователя:")
		main_layout.addWidget(self.id_label)
		
		self.id_line = QLineEdit(self)
		self.id_line.setText('ID')
		self.id_line.setReadOnly(True)
		main_layout.addWidget(self.id_line)
		
		self.login_label = QLabel("Логин пользователя:")
		main_layout.addWidget(self.login_label)
		
		self.login_line = QLineEdit(self)
		self.login_line.setText('login')
		main_layout.addWidget(self.login_line)
		
		self.login_label = QLabel("Пароль пользователя:")
		main_layout.addWidget(self.login_label)
		
		self.password_line = QLineEdit(self)
		self.password_line.setText('password')
		main_layout.addWidget(self.password_line)
		
		self.edit_user_button = QPushButton("Изменить пользователя", self)
		self.edit_user_button.clicked.connect(self.edit_user)
		main_layout.addWidget(self.edit_user_button)

		self.del_user_button = QPushButton("Удалить пользователя", self)
		self.del_user_button.clicked.connect(self.del_user)
		main_layout.addWidget(self.del_user_button)
		
		self.add_user_button = QPushButton("Добавить пользователя", self)
		self.add_user_button.clicked.connect(self.add_user)
		main_layout.addWidget(self.add_user_button)
		
		self.show_tasks_button = QPushButton("Показать задачи пользователя", self)
		self.show_tasks_button.clicked.connect(self.show_tasks)
		self.show_tasks_button.setEnabled(False)
		main_layout.addWidget(self.show_tasks_button)
			
		self.update_users()
		
	def check_input_data(self):
		name = self.name_line.text().strip()
		surname = self.surname_line.text().strip()
		thirdname = self.thirdname_line.text().strip()
		login = self.login_line.text().strip()
		password = self.password_line.text().strip()
		return name and surname and thirdname and login and password
		
	def add_user(self):
		if not self.check_input_data():
			showDialog("Ошибка", "Не полностью введены данные о пользователе")
			return
		data = {
			"name": self.name_line.text().strip(),
			"surname": self.surname_line.text().strip(),
			"thirdName": self.thirdname_line.text().strip(),
			"login": self.login_line.text().strip(),
			"password": self.password_line.text().strip(),
		}
		request_answer = send_request("add_user", data)
		if request_answer['success']:
			self.update_users()
		else:
			showDialog("Ошибка", "Логин пользователя не уникален", False)
		
	def edit_user(self):
		data = {
			"id": self.id_line.text(),
			"name": self.name_line.text(),
			"surname": self.surname_line.text(),
			"thirdName": self.thirdname_line.text(),
			"login": self.login_line.text(),
			"password": self.password_line.text(),
		}
		request_answer = send_request("edit_user", data)
		if request_answer['success']:
			self.update_users()
		else:
			showDialog("Ошибка", "Логин пользователя не уникален", False)

	def update_users(self):
		users = send_request("list_users", {})
		self.users = list(users['users'])
		self.users_list.clear()
		for user in self.users:
			self.users_list.addItem(user['name'] + " " + user['surname'] + " " + user['thirdName'])
		self.edit_user_button.setEnabled(bool(self.users))
		self.del_user_button.setEnabled(bool(self.users))
		self.show_tasks_button.setEnabled(bool(self.users))
			
	def index_changed(self, index):
		if index>=0:
			self.user = self.users[index]
			self.fill_user_data()
			self.show_tasks_button.setEnabled(True)
		
	def show_tasks(self):
		self.user_window = UserWindow(self.user['id'])
		self.user_window.show()
				
	def fill_user_data(self):
		self.name_line.setText(self.user['name'])
		self.surname_line.setText(self.user['surname'])
		self.thirdname_line.setText(self.user['thirdName'])
		self.id_line.setText(str(self.user['id']))
		self.login_line.setText(self.user['login'])
		self.password_line.setText(self.user['password'])
			
	def del_user(self):
		data = {
			"userID" : self.id_line.text()
		}
		send_request("delete_user", data)
		self.update_users()
