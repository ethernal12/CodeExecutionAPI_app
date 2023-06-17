from pathlib import Path

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QComboBox, QListView, QLabel, QTextEdit, QPushButton


class Ui_CEAA(QtWidgets.QMainWindow):

	def __init__(self):
		super(Ui_CEAA, self).__init__()
		path = str(Path(__file__).parent.joinpath("GUI.ui").resolve().absolute())
		uic.loadUi(path, self)

		submitBtn: QPushButton
		codingTE: QTextEdit
		test1LB: QLabel
		test2LB: QLabel
		test3LB: QLabel


if __name__ == "__main__":
	import sys

	Qapp = QtWidgets.QApplication(sys.argv)
	mainui = Ui_CEAA()
	mainui.show()
	Qapp.exec()
