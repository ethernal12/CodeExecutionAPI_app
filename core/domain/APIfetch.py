import base64
import binascii
import os
import time

import requests
from dotenv import load_dotenv

import core.utils
from core import utils

load_dotenv()
X_RAPIDAPI_KEY = os.environ['X_RAPIDAPI_KEY']
X_RAPIDAPI_HOST = os.environ['X_RAPIDAPI_HOST']


def getLanguages():
	url = "https://judge0-ce.p.rapidapi.com/languages"

	headers = {
		"X-RapidAPI-Key": X_RAPIDAPI_KEY,
		"X-RapidAPI-Host": X_RAPIDAPI_HOST
	}

	response = requests.get(url, headers=headers)

	print(response.json())


def makeSubmission(code):
	# Zakodiraj na base64

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
		"X-RapidAPI-Key": X_RAPIDAPI_KEY,
		"X-RapidAPI-Host": X_RAPIDAPI_HOST
	}


	response = requests.post(url, json=payload, headers=headers, params=querystring)

	if response.status_code == 201:

		token = response.json()['token']
		return getSubmission(token)
	else:
		print("Failed to create submission.")


def makeBatchSubmission(code):
	naloga = 'Naloga 1'
	dobiInputeNaloge = core.utils.extract_cases(naloga, 'Input')

	url = "https://judge0-ce.p.rapidapi.com/submissions/batch"

	querystring = {"base64_encoded": "True", "fields": "*"}

	payload = {"submissions": [
		{
			"language_id": 71,
			"source_code": code,
			"stdin": dobiInputeNaloge[0]
		},
		{
			"language_id": 71,
			"source_code": code,
			"stdin": dobiInputeNaloge[1]
		},
		{
			"language_id": 71,
			"source_code": code,
			"stdin": dobiInputeNaloge[2]
		}
	]}
	headers = {
		'content-type': 'application/json',
		'Content-Type': 'application/json',
		"X-RapidAPI-Key": X_RAPIDAPI_KEY,
		"X-RapidAPI-Host": X_RAPIDAPI_HOST
	}

	try:
		response = requests.post(url, json=payload, headers=headers, params=querystring)
		response.raise_for_status()  # za ne-2xx statusne napake

		if response.status_code == 201:
			response_data = response.json()
			results = []
			for item in response_data:
				token = item['token']
				# sem probal sekundo timeout ampak je premalo, prvi output ni nikoli procesiran
				time.sleep(2)
				result = getSubmission(token)
				con_res = utils.removeNewLine(result)
				results.append(con_res)
			return results
		else:
			print("Failed to create submission.")

	except requests.exceptions.RequestException as e:
		print("Pojavila se je napaka:", str(e))


def getSubmission(token):
	url = f"https://judge0-ce.p.rapidapi.com/submissions/{token}"
	querystring = {"base64_encoded": "true", "fields": "*"}

	headers = {
		"X-RapidAPI-Key": X_RAPIDAPI_KEY,
		"X-RapidAPI-Host": X_RAPIDAPI_HOST
	}

	response = requests.get(url, headers=headers, params=querystring)
	if response.json()['stdout']:

		try:
			decoded_output = base64.b64decode(response.json()['stdout']).decode('utf-8')

			return decoded_output
		except binascii.Error as e:
			print(f"Error decoding base64: {e}")
			return None
	# če je napaka v sintaksi
	elif response.json()['stderr']:
		stderr = base64.b64decode(response.json()['stderr']).decode('utf-8')
		raise Exception(stderr)
