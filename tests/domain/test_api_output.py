import unittest

from core import utils


class Test_api_output(unittest.TestCase):
	def setUp(self) -> None:
		self.resitev = 'Resitev 1'
		self.dobiOutputUcenca = utils.extract_output()
		self.resitveNalog = utils.extract_cases(self.resitev, "Output")
		self.napake = []

	def test_response(self):
		for i, (response, expected_response) in enumerate(zip(self.dobiOutputUcenca, self.resitveNalog), start=1):
			try:
				self.assertEqual(response, expected_response)
				print(f"Assertion {i} passed.")
			except AssertionError:
				napaka = f"Assertion {i} failed: {response} != {expected_response}"
				self.napake.append(napaka)
		if self.napake:
			self.fail('\n'.join(self.napake))

if __name__ == '__main__':
	unittest.main()
