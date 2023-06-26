import os
import subprocess
import sys
from pathlib import Path

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QLabel, QTextEdit, QPushButton

from core.domain import APIfetch, AWSLambda, tio

sys.path.append(os.getcwd())


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

	def aws_lambda(self):
		print('aws lambda')
		AWSLambda.invoke_lambda_function()

	def run_tio(self):
		tio.run_tio()

	def APIfetch(self):
		# dobi kodo iz text inputa in pretvori v tekst
		code = self.codingTE.toPlainText()
		try:
			responses = APIfetch.makeBatchSubmission(code)
			print(responses, 'response from gui')
			with open('../core/responsi.txt', 'w') as file:
				for response in responses:
					file.write(response + '\n')
			# Zazeni teste
			# command = "python -m unittest discover tests"
			# print('uspešno vrnil API response, poganjam teste...')
			# subprocess.run(command, shell=True)
		except Exception as e:
			print(f"Napaka v sintaksi kode: {str(e)}")


# if match == -1:
# 	# Set green background for all labels
# 	self.set_label_background_color(self.test1LB, QColor("green"))
# 	self.set_label_background_color(self.test2LB, QColor("green"))
# 	self.set_label_background_color(self.test3LB, QColor("green"))
# elif match:
# 	if 0 in match:
#
# 		self.set_label_background_color(self.test1LB, QColor("red"))
# 	else:
# 		self.set_label_background_color(self.test1LB, QColor("green"))
# 	if 1 in match:
#
# 		self.set_label_background_color(self.test2LB, QColor("red"))
# 	else:
# 		self.set_label_background_color(self.test2LB, QColor("green"))
# 	if 2 in match:
#
# 		self.set_label_background_color(self.test3LB, QColor("red"))
# 	else:
# 		self.set_label_background_color(self.test3LB, QColor("green"))


if __name__ == "__main__":
	import sys

	Qapp = QtWidgets.QApplication(sys.argv)
	mainui = Ui_CEAA()
	mainui.show()
	Qapp.exec()
