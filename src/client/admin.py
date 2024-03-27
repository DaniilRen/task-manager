#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys
from admin_window import AdminWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = AdminWindow()
	window.show()
	app.exec()
