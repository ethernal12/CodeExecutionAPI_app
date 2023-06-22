import unittest

from core import utils


class Test_api_output(unittest.TestCase):
	def setUp(self) -> None:
		self.resitev = 'Resitev 1'
		self.dobiOutputUcenca = utils.extract_output()
		self.resitveNalog = utils.extract_cases(self.resitev, "Output")
		self.failures = []

	def test_response(self):
		for i, (response, expected_response) in enumerate(zip(self.dobiOutputUcenca, self.resitveNalog), start=1):
			try:
				self.assertEqual(response, expected_response)
				print(f"Assertion {i} passed.")
			except AssertionError:
				failure = f"Assertion {i} failed: {response} != {expected_response}"
				self.failures.append(failure)
		if self.failures:
			self.fail('\n'.join(self.failures))

		if __name__ == '__main__':
			unittest.main()
