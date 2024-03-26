#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from library import send_request
from user_window import UserWindow


class AdminWindow(QMainWindow):
	
	def __init__(self):
		super().__init__()
		
		window_position = (200, 200)
		size_gap = 10
		window_width = 600
		window_height = 700
		data_width = window_width - size_gap * 2
		raw_data_height = size_gap * 10
		line_height = size_gap * 3
		old_y = size_gap
		y_coord = old_y + size_gap
		
		# Set window properties
		self.setWindowTitle("Клиент администратора")

		# Create GUI components
		self.users_list = QComboBox(self)
		self.users_list.setGeometry(size_gap, y_coord, data_width, line_height)
		self.users_list.currentIndexChanged.connect(self.index_changed)
		y_coord += size_gap + line_height
		
		self.name_line = QLineEdit(self)
		self.name_line.setGeometry(size_gap, y_coord, data_width, line_height)
		self.name_line.setText('Имя')
		y_coord += size_gap + line_height
		
		self.surname_line = QLineEdit(self)
		self.surname_line.setGeometry(size_gap, y_coord, data_width, line_height)
		self.surname_line.setText('Фамилия')
		y_coord += size_gap + line_height
		
		self.thirdname_line = QLineEdit(self)
		self.thirdname_line.setGeometry(size_gap, y_coord, data_width, line_height)
		self.thirdname_line.setText('Отчество')
		y_coord += size_gap + line_height
		
		self.id_line = QLineEdit(self)
		self.id_line.setGeometry(size_gap, y_coord, data_width, line_height)
		self.id_line.setText('ID')
		self.id_line.setReadOnly(True)
		y_coord += size_gap + line_height
		
		self.login_line = QLineEdit(self)
		self.login_line.setGeometry(size_gap, y_coord, data_width, line_height)
		self.login_line.setText('login')
		y_coord += size_gap + line_height
		
		self.password_line = QLineEdit(self)
		self.password_line.setGeometry(size_gap, y_coord, data_width, line_height)
		self.password_line.setText('password')
		y_coord += size_gap + line_height
		
		self.edit_user_button = QPushButton("Изменить пользователя", self)
		self.edit_user_button.setGeometry(size_gap, y_coord, data_width, line_height)
		self.edit_user_button.clicked.connect(self.edit_user)
		y_coord += size_gap + line_height

		self.del_user_button = QPushButton("Удалить пользователя", self)
		self.del_user_button.setGeometry(size_gap, y_coord, data_width, line_height)
		self.del_user_button.clicked.connect(self.del_user)
		y_coord += size_gap + line_height
		
		self.add_user_button = QPushButton("Добавить пользователя", self)
		self.add_user_button.setGeometry(size_gap, y_coord, data_width, line_height)
		self.add_user_button.clicked.connect(self.add_user)
		y_coord += size_gap + line_height
		
		self.show_tasks_button = QPushButton("Показать задачи пользователя", self)
		self.show_tasks_button.setGeometry(size_gap, y_coord, data_width, line_height)
		self.show_tasks_button.clicked.connect(self.show_tasks)
		self.show_tasks_button.setEnabled(False)
		y_coord += size_gap + line_height
		
		if not self.check_connection():
			self.showDialog("Ошибка", "Нет соединения с сервером")
			exit(1)
			
		self.update_users()
		self.setGeometry(window_position[0], window_position[1], window_width, y_coord)
		
	def check_connection(self):
		# ~ TODO rewrite this
		return True

	def add_user(self):
		data = {
			"name": self.name_line.text(),
			"surname": self.surname_line.text(),
			"thirdName": self.thirdname_line.text(),
			"login": self.login_line.text(),
			"password": self.password_line.text(),
		}
		send_request("add_user", data)
		self.update_users()
		
	def edit_user(self):
		data = {
			"id": self.id_line.text(),
			"name": self.name_line.text(),
			"surname": self.surname_line.text(),
			"thirdName": self.thirdname_line.text(),
			"login": self.login_line.text(),
			"password": self.password_line.text(),
		}
		send_request("edit_user", data)
		self.update_users()

	def update_users(self):
		users = send_request("list_users", {})
		self.users = list(users['users'])
		self.users_list.clear()
		for user in self.users:
			self.users_list.addItem(user['name'] + " " + user['surname'] + " " + user['thirdName'])
		self.edit_user_button.setEnabled(bool(self.users))
			
	def index_changed(self, index):
		self.user = self.users[index]
		self.fill_user_data()
		self.show_tasks_button.setEnabled(True)
		
	def show_tasks(self):
		user_id = self.user['id']
		self.user_window = UserWindow(user_id)
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
		self.list_users()
