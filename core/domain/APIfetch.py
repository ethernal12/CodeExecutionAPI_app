import base64
import binascii
import time

import requests

import core.utils
from dotenv import load_dotenv
import os

load_dotenv()
def getLanguages():
	X_RAPIDAPI_KEY = os.environ['X_RAPIDAPI_KEY']
	X_RAPIDAPI_HOST = os.environ['X_RAPIDAPI_HOST']
	url = "https://judge0-ce.p.rapidapi.com/languages"

	headers = {
		"X-RapidAPI-Key": X_RAPIDAPI_KEY,
		"X-RapidAPI-Host": X_RAPIDAPI_HOST
	}

	response = requests.get(url, headers=headers)

	print(response.json())


def makeSubmission(code):
	# Encode the code using base64

	url = "https://judge0-ce.p.rapidapi.com/submissions"

	querystring = {"base64_encoded": "True", "fields": "*"}

	payload = {
		"language_id": 71,
		"source_code": code,
		"stdin": "1 2 3 4 5\n"
	}
	headers = {
		'content-type': 'application/json',
		'Content-Type': 'application/json',
		"X-RapidAPI-Key": "83758d9391msh1eae830eea126bdp1cdcc6jsn3c5dde0aa62c",
		"X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
	}
	# Convert payload to JSON string

	response = requests.post(url, json=payload, headers=headers, params=querystring)

	# Check the response status
	if response.status_code == 201:
		# get the token created from post response and get the code output
		token = response.json()['token']
		return getSubmission(token)
	else:
		print("Failed to create submission.")
		print(f"Response: {response.text}")


def makeBatchSubmission(code):
	task = 'Task 1'
	extractCases = core.utils.extract_cases(task)

	url = "https://judge0-ce.p.rapidapi.com/submissions/batch"

	querystring = {"base64_encoded": "True", "fields": "*"}

	payload = {"submissions": [
		{
			"language_id": 71,
			"source_code": code,
			"stdin": core.utils.convert_to_string(extractCases[0])
		},
		{
			"language_id": 71,
			"source_code": code,
			"stdin": core.utils.convert_to_string(extractCases[1])
		},
		{
			"language_id": 71,
			"source_code": code,
			"stdin": core.utils.convert_to_string(extractCases[2])
		}
	]}
	headers = {
		'content-type': 'application/json',
		'Content-Type': 'application/json',
		"X-RapidAPI-Key": X_RAPIDAPI_KEY,
		"X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
	}
	# Convert payload to JSON string

	response = requests.post(url, json=payload, headers=headers, params=querystring)

	# Check the response status
	if response.status_code == 201:
		# get the token created from post response and get the code output
		response_data = response.json()
		results = []  # Create an empty list to store the results

		for item in response_data:
			token = item['token']
			time.sleep(2)
			result = getSubmission(token)
			results.append(result)  # Store the result in the list

		return results  # Return the list of results after the loop

	else:
		print("Failed to create submission.")
		print(f"Response: {response.text}")


def getSubmission(token):
	url = f"https://judge0-ce.p.rapidapi.com/submissions/{token}"
	querystring = {"base64_encoded": "true", "fields": "*"}

	headers = {
		"X-RapidAPI-Key": X_RAPIDAPI_KEY,
		"X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)
	if response.json()['stdout']:

		try:
			decoded_output = base64.b64decode(response.json()['stdout']).decode('utf-8')
			return decoded_output
		except binascii.Error as e:
			print(f"Error decoding base64: {e}")
			return None  # Handle the error case appropriately

	elif response.json()['stderr']:
		stderr = base64.b64decode(response.json()['stderr']).decode('utf-8')
		return stderr
