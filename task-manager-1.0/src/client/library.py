#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys
import subprocess
import json
import requests

from PyQt5.QtWidgets import QMessageBox

from enum import Enum
from enum import auto


class TaskStatus(Enum):
	ASSIGNED = (0, "Назначена")
	IN_WORK = (1, "В работе")
	DONE  = (2, "Завершена")


def open_file(filename):
    if sys.platform == 'win32':
        subprocess.run(['start', '', filename], shell=True)
    elif sys.platform == 'darwin':
        subprocess.run(['open', filename])
    else:
        subprocess.run(['xdg-open', filename])


def showDialog(title, text, use_exit=True):
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Information)
	msgBox.setText(text)
	msgBox.setWindowTitle(title)
	msgBox.setStandardButtons(QMessageBox.Ok)
	returnValue = msgBox.exec()
	if use_exit and returnValue == QMessageBox.Ok:
		print("Exiting", use_exit)
		exit()
		
def get_url():
	with open('config.json') as file:
		data = json.load(file)
	return data['url']
		
def send_request(endpoint, data):
	url = get_url() + endpoint
	headers = {
		"Content-Type": "application/json",
		"Accept": "application/json"
	}
	answer = None
	try:
		print("Sending", endpoint, data)
		response = requests.post(url, headers=headers, json=data)
		if response.status_code == 200:
			print("Server response", response.text)
			answer = json.loads(response.text)
		else:
			showDialog("Ошибка", "Ошибка соединения с сервером")
			print(f"Error: Request failed with status code {response.status_code}")
	except requests.exceptions.RequestException as err:
		showDialog("Ошибка", f"Ошибка соединения с сервером {str(err)}")
	return answer


class Task:
	
	def __init__(self, task_id, name, description, task_class, task_status):
		self.task_id = task_id
		self.name = name
		self.description = description
		self.task_class = task_class
		self.task_status = task_status


class Blob:
	
	def __init__(self, blob_id, file_name, blob_data):
		self.blob_id = blob_id 
		self.file_name = file_name
		self.blob_data = blob_data
