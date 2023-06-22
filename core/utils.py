import os


def convert_to_string(numbers):
	# moram convertat ker pravi format je "1 2 3 4 5"
	numbers_str = ' '.join(map(str, numbers)) + '\n'
	return numbers_str


def extract_cases(st_naloge, input_output):
	current_dir = os.path.dirname(os.path.abspath(__file__))
	cases = []
	with open(f'{current_dir}/taskCases.txt', 'r') as file:
		lines = file.readlines()
		current_task = None
		for line in lines:
			if line.startswith(st_naloge):
				current_task = line.strip()
			elif current_task == st_naloge and line.startswith(input_output):
				case = line.split(':')[1].strip()
				cases.append(eval(case))
	return cases

def extract_output():
	current_dir = os.path.dirname(os.path.abspath(__file__))
	outputs = []
	with open(f'{current_dir}/responsi.txt', 'r') as file:
		lines = file.readlines()
		for line in lines:
			# rstrip() odstrani newline \n iz stringa
			toString = ''.join(line.rstrip())
			outputs.append(toString)
	return outputs



def removeNewLine(data):
	data_without_newlines = ''.join(data).replace('\n', '')
	return data_without_newlines

