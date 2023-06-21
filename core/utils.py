def convert_to_string(numbers):
	numbers_str = ' '.join(map(str, numbers)) + '\n'
	return numbers_str


def extract_cases(task_name):
	cases = []
	with open('../core/taskCases.txt', 'r') as file:
		lines = file.readlines()
		current_task = None
		for line in lines:
			if line.startswith('Task'):
				current_task = line.strip()
			elif current_task == task_name and line.startswith('Case'):
				case = line.split(':')[1].strip()
				cases.append(eval(case))
	return cases


def removeNewLine(data):
	data_without_newlines = [string.replace('\n', '') for string in data]
	return data_without_newlines


def find_non_matching_index(array1, array2):
	print(len(array1), len(array2))
	match_array = []
	for i in range(len(array1)):
		if array1[i] != array2[i]:
			match_array.append(i)
	if match_array:
		return match_array
	else:
		return -1
