from core import utils


def test_response(response):
	withoutNewLine = utils.removeNewLine(response)
	task = 'Task 1'
	getAllCases = utils.extract_cases(task)

	generateResponse = []
	for case in getAllCases:
		response = ""
		for number in case:
			absNum = abs(number)
			if absNum % 2 == 0:
				response += "S"
			else:
				response += "L"
		generateResponse.append(response)
	match = utils.find_non_matching_index(withoutNewLine, generateResponse)
	return match

