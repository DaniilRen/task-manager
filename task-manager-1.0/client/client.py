#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys

from admin_window import AdminWindow
from user_window import UserWindow
from user_window import LoginWindow

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel


if __name__ == "__main__":
	app = QApplication(sys.argv)
	if len(sys.argv) == 2:
		window = AdminWindow()
	else:
		window = LoginWindow()
	window.show()
	app.exec()
