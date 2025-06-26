#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog

from library import send_request
from library import Task
from library import Blob
from library import TaskStatus
from library import showDialog
from library import open_file

import base64
import os



class LoginWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("Login Window")
		self.setGeometry(300, 300, 300, 150)

		self.login_label = QLabel("Имя пользователя:")
		self.login_input = QLineEdit()
		
		self.password_label = QLabel("Пароль:")
		self.password_input = QLineEdit()
		self.password_input.setEchoMode(QLineEdit.Password)

		self.ok_button = QPushButton("Принять")
		self.ok_button.clicked.connect(self.handle_ok_button)
		
		self.cancel_button = QPushButton("Отмена")
		self.cancel_button.clicked.connect(self.close)

		layout = QVBoxLayout()
		layout.addWidget(self.login_label)
		layout.addWidget(self.login_input)
		layout.addWidget(self.password_label)
		layout.addWidget(self.password_input)
		layout.addWidget(self.ok_button)
		layout.addWidget(self.cancel_button)

		self.setLayout(layout)
		
		self.show()
        
	def handle_ok_button(self):
		login = self.login_input.text().strip()
		password = self.password_input.text().strip()
		if not login or not password:
			showDialog("Ошибка", "Не задан логин или пароль", False)
		else:
			data = {
				"login": login, 
				"password": password
			}
			user_data = send_request("get_user_by_credentials", data)
			if user_data['success']:
				user_id = user_data['userId']
				self.user_window = UserWindow(user_id)
				self.user_window.show()
				self.close()
			else:
				showDialog("Ошибка", "Пользователь с таким именем или паролем не найден", False)
			

class UserWindow(QWidget):
	
	def __init__(self, user_id=None):
		super().__init__()
		assert user_id or credentials
		self.downloads_folder = "downloads"
		os.makedirs(self.downloads_folder, exist_ok=True)
		self.tasks = []
		self.blobs = []
		self.setWindowTitle("Клиент пользователя")
		self.setFixedSize(640, 480)  # Non-resizable window
		self.user_id = user_id
		assert self.user_id
		self.setup_ui()
		self.get_tasks_for_user()
		
	def setup_left_column(self, main_layout):
		# Left column
		left_layout = QVBoxLayout()
		
		self.task_class_label = QLabel("Фильтрация по классу задачи:")
		left_layout.addWidget(self.task_class_label)
		
		self.task_categories_cbox = QComboBox()
		self.task_categories_cbox.currentIndexChanged.connect(self.category_index_changed)
		left_layout.addWidget(self.task_categories_cbox)
		
		self.task_list_widget_label = QLabel("Список задач:")
		left_layout.addWidget(self.task_list_widget_label)
		
		self.task_list_widget = QListWidget()
		self.task_list_widget.clicked.connect(self.on_task_list_clicked)
		left_layout.addWidget(self.task_list_widget)
		
		self.task_status_label = QLabel("Статус задачи:")
		left_layout.addWidget(self.task_status_label)
		
		self.task_status_cbox = QComboBox()
		for member in TaskStatus:
			self.task_status_cbox.addItem(member.value[1])
		left_layout.addWidget(self.task_status_cbox)
		
		self.task_class_label = QLabel("Класс текущей задачи:")
		left_layout.addWidget(self.task_class_label)
		
		self.task_class_line = QLineEdit()
		left_layout.addWidget(self.task_class_line)
		
		self.button_update = QPushButton("Сохранить задачу")
		self.button_update.clicked.connect(self.edit_task)
		left_layout.addWidget(self.button_update)
		
		self.button_add = QPushButton("Добавить задачу")
		self.button_add.clicked.connect(self.add_task)
		left_layout.addWidget(self.button_add)
		
		self.button_delete = QPushButton("Удалить задачу")
		self.button_delete.clicked.connect(self.delete_task)
		left_layout.addWidget(self.button_delete)
		
		main_layout.addLayout(left_layout)
		
	def setup_right_column(self, main_layout):
		# Right column
		right_layout = QVBoxLayout()
		
		self.task_name_label = QLabel("Название задачи:")
		right_layout.addWidget(self.task_name_label)
		
		self.task_name_line = QLineEdit()
		right_layout.addWidget(self.task_name_line)
		
		self.description_label = QLabel("Описание задачи:")
		right_layout.addWidget(self.description_label)

		self.task_description = QTextEdit()
		right_layout.addWidget(self.task_description)
		
		self.file_list_widget_label = QLabel("Список файлов задачи:")
		right_layout.addWidget(self.file_list_widget_label)
		
		self.blob_list_widget = QListWidget()
		self.blob_list_widget.clicked.connect(self.on_blob_list_clicked)
		right_layout.addWidget(self.blob_list_widget)
		
		self.button_add_file = QPushButton("Добавить файл")
		self.button_add_file.setEnabled(False)
		self.button_add_file.clicked.connect(self.add_blob)
		right_layout.addWidget(self.button_add_file)
		
		self.button_delete_file = QPushButton("Удалить файл")
		self.button_delete_file.setEnabled(False)
		self.button_delete_file.clicked.connect(self.delete_blob)
		right_layout.addWidget(self.button_delete_file)

		main_layout.addLayout(right_layout)
		
	def setup_ui(self):
		main_layout = QHBoxLayout(self)
		main_layout.setContentsMargins(10, 10, 10, 10)
		
		self.setup_left_column(main_layout)
		self.setup_right_column(main_layout)
		
	def populate_widgets(self):
		self.task_class_line.clear()
		self.task_name_line.clear()
		self.task_description.clear()
		self.task_categories_cbox.clear()
		for task_category in self.get_task_categories():
			self.task_categories_cbox.addItem(task_category)
		self.category_index_changed()
		self.on_task_list_clicked()
			
	def category_index_changed(self):
		self.button_add_file.setEnabled(False)
		self.button_delete_file.setEnabled(False)
		self.task_list_widget.clear()
		self.task_list_widget.addItems([task.name for task in self.tasks if task.task_class == self.task_categories_cbox.currentText()])
		self.blob_list_widget.clear()
	
	def on_task_list_clicked(self):
		selected_row = self.task_list_widget.currentRow()
		if selected_row >= 0:
			task = self.tasks[selected_row]
			self.task_id = task.task_id
			print("Current task id is", self.task_id)
			self.task_name_line.setText(task.name)
			self.task_description.setPlainText(task.description)
			self.task_class_line.setText(task.task_class)
			for member in TaskStatus:
				if member.name == task.task_status:
					self.task_status_cbox.setCurrentIndex(member.value[0])
			self.button_add_file.setEnabled(True)
			self.get_blobs_for_task()
	
	def on_blob_list_clicked(self):
		selected_row = self.blob_list_widget.currentRow()
		if selected_row >= 0:
			blob = self.blobs_for_task[selected_row]
			output_file_path = os.path.join(self.downloads_folder, blob.file_name)
			if not os.path.exists(output_file_path):
				decoded_data = base64.b64decode(blob.blob_data)
				with open(output_file_path, 'wb') as file:
					file.write(decoded_data)
			open_file(output_file_path)
			self.button_delete_file.setEnabled(True)
		
	def get_current_task_status_from_ui(self):
		enum_mapping = {member.value[1]: member for member in TaskStatus}
		selected_text = self.task_status_cbox.currentText()
		selected_enum = enum_mapping[selected_text]
		return selected_enum.name
		
	def get_tasks_for_user(self):
		data = {
			"userId": self.user_id
		}
		tasks_for_user = send_request("get_tasks_for_user", data)
		self.tasks = []
		for task in tasks_for_user['taskList']:
			task_id = task['id']
			name = task['name']
			description = task['description']
			task_class = task['taskClass']
			task_status = task['taskStatus']
			task = Task(task_id, name, description, task_class, task_status)
			self.tasks.append(task)
		self.populate_widgets()
			
	def get_blobs_for_task(self):
		data = {
			"taskId": self.task_id
		}
		blobs_for_task = send_request("get_blobs_for_task", data)
		self.blobs_for_task = []
		for blob in blobs_for_task['blobList']:
			blob_id = blob['id']
			file_name = blob['fileName']
			blob_data = blob['blobData']
			self.blobs_for_task.append(Blob(blob_id, file_name, blob_data))
		self.blob_list_widget.clear()
		self.blob_list_widget.addItems([blob.file_name for blob in self.blobs_for_task])
			
	def get_task_categories(self):
		return {task.task_class for task in self.tasks}
		
	def check_input_data(self):
		if not bool(self.task_class_line.text().strip()):
			showDialog("Ошибка", "Не задан класс задачи", False)
			return False
		if not bool(self.task_name_line.text().strip()):
			showDialog("Ошибка", "Не задано имя задачи", False)
			return False
		return True
		
	def edit_task(self):
		if not self.check_input_data():
			return 
		selected_row = self.task_list_widget.currentRow()
		if selected_row is not None:
			data = {
				"name": self.task_name_line.text(),
				"description": self.task_description.toPlainText(),
				"taskId": self.task_id,
				"taskClass": self.task_class_line.text(),
				"taskStatus": self.get_current_task_status_from_ui()
			}
			send_request("edit_task", data)
			self.get_tasks_for_user()
			
	def delete_task(self):
		selected_row = self.task_list_widget.currentRow()
		if selected_row is not None:
			data = {
				"taskID": self.tasks[selected_row].task_id
			}
			send_request("delete_task", data)
		self.get_tasks_for_user()
		
	def get_task_class_from_ui(self):
		return self.task_categories_cbox.currentText()
		
	def add_task(self):
		number = str(len(self.tasks) + 1)
		name = "Задача " + number
		userID = self.user_id
		data = {
				"name": name,
				"description": "Описание задачи " + number,
				"userId": self.user_id,
				"taskClass": "Рабочая задача",
				"taskStatus": self.get_current_task_status_from_ui()
			}
		send_request("add_task", data)
		self.get_tasks_for_user()
		
	def add_blob(self):
		selected_row = self.task_list_widget.currentRow()
		if selected_row >= 0:
			options = QFileDialog.Options()
			file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)", options=options)
			if file_path:
				with open(file_path, 'rb') as file:
					binary_data = file.read()
				encoded_data = base64.b64encode(binary_data).decode('utf-8')
				data = {
					"taskId": self.tasks[selected_row].task_id,
					"fileName": os.path.basename(file_path),
					"blobData": encoded_data
				}
				send_request("add_blob", data)
				self.get_blobs_for_task()
	
	def delete_blob(self):
		selected_row = self.blob_list_widget.currentRow()
		if selected_row >= 0:
			data = {
				"blobId": self.blobs_for_task[selected_row].blob_id
			}
			send_request("delete_blob", data)
			self.get_blobs_for_task()
			self.button_delete_file.setEnabled(False)
