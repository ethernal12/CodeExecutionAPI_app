from pathlib import Path

from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QTextEdit, QPushButton

from core.domain import APIfetch, tests


class Ui_CEAA(QtWidgets.QMainWindow):
	submitBtn: QPushButton

	codingTE: QTextEdit
	test1LB: QLabel
	test2LB: QLabel
	test3LB: QLabel

	def __init__(self):
		super(Ui_CEAA, self).__init__()
		path = str(Path(__file__).parent.joinpath("GUI.ui").resolve().absolute())
		uic.loadUi(path, self)

		self.setupUi()

	def setupUi(self):
		self.submitBtn.clicked.connect(self.APIfetch)

	def set_label_background_color(self, label, color):
		label.setAutoFillBackground(True)
		palette = label.palette()
		palette.setColor(label.backgroundRole(), color)
		label.setPalette(palette)

	def APIfetch(self):
		code = self.codingTE.toPlainText()
		# response = APIfetch.makeSubmission(code)
		# response = APIfetch.getLanguages()
		response = APIfetch.makeBatchSubmission(code)

		match = tests.test_response(response=response)
		print(type(match))
		if match == -1:
			# Set green background for all labels
			self.set_label_background_color(self.test1LB, QColor("green"))
			self.set_label_background_color(self.test2LB, QColor("green"))
			self.set_label_background_color(self.test3LB, QColor("green"))
		elif match:
			if 0 in match:
				# Set red background for test1LB
				self.set_label_background_color(self.test1LB, QColor("red"))
			else:
				self.set_label_background_color(self.test1LB, QColor("green"))
			if 1 in match:
				# Set red background for test2LB
				self.set_label_background_color(self.test2LB, QColor("red"))
			else:
				self.set_label_background_color(self.test2LB, QColor("green"))
			if 2 in match:
				# Set red background for test3LB
				self.set_label_background_color(self.test3LB, QColor("red"))
			else:
				self.set_label_background_color(self.test3LB, QColor("green"))


if __name__ == "__main__":
	import sys

	Qapp = QtWidgets.QApplication(sys.argv)
	mainui = Ui_CEAA()
	mainui.show()
	Qapp.exec()
