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

from json import load, dump
from re import fullmatch


class ConfWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.cfg_path = "config.json"
        
        self.setFixedSize(400, 200)
        
        # Set window properties
        self.setWindowTitle("Конфигурация сети")
        
        main_layout = QVBoxLayout(self)
        margin = 5
        main_layout.setContentsMargins(margin, margin, margin, margin)

        # Create GUI components        
        self.info_label = QLabel("""Важно: адрес должен вводиться полностью,\nвместе с указанием сетевого протокола, порта и указателя /api/.\nНапример: http://192.168.0.1:8080/api/ или http://localhost:8080/api/""")
        main_layout.addWidget(self.info_label)

        self.address_label = QLabel("адрес сети:")
        main_layout.addWidget(self.address_label)
        
        self.address_line = QLineEdit(self)
        self.address_line.setText(self.load_address())
        main_layout.addWidget(self.address_line)
        
        
        self.save_button = QPushButton("Применить настройки", self)
        self.save_button.clicked.connect(self.update_conf)
        main_layout.addWidget(self.save_button)


    # loads data from conf file
    def load_address(self):
        with open(self.cfg_path) as cfg:
            return load(cfg)["url"] 

        
    def check_input_data(self):
        return fullmatch(
            r"^(http|https):\/\/([a-zA-Z0-9.-]+|\d{1,3}(?:\.\d{1,3}){3})(:\d{1,5})?\/api\/$", 
            self.address_line.text().strip()
            )

        
    def update_conf(self):
        if not self.check_input_data():
            showDialog("Ошибка", "Адрес указан некорректно")
            return
        new_cfg = {
            "url": self.address_line.text().strip(),
        }
        with open(self.cfg_path, 'w') as cfg:
            dump(new_cfg, cfg, indent=4)
            showDialog("Измененя сохранены", "Конфигурация сети успешно изменена")
        