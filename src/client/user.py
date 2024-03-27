#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys
from user_window import LoginWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = LoginWindow()
	window.show()
	app.exec()
