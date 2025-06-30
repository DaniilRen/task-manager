#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys

from conf_window import ConfWindow

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = ConfWindow()
	window.show()
	app.exec()
