import os
import time

import requests
from dotenv import load_dotenv

import core.utils

load_dotenv()
X_RAPIDAPI_KEY = os.environ['X_RAPIDAPI_KEY']
X_RAPIDAPI_HOST = os.environ['X_RAPIDAPI_HOST']


def getLanguages():
	print('--------------------------------------------------get language id')
	url = "https://judge0-ce.p.rapidapi.com/languages"

	headers = {
		"X-RapidAPI-Key": X_RAPIDAPI_KEY,
		"X-RapidAPI-Host": X_RAPIDAPI_HOST
	}
	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()

	except requests.exceptions.RequestException as e:
		print("Pojavila se je napaka:", str(e))

	return response.json()


def makeBatchSubmission(code):
	print('--------------------------------------------------make batched submission')
	liste_prog_jezikov = getLanguages()
	izbrani_prog_jezik = 'Python (3.8.1)'

	id_prog_jezika = ''
	for language in liste_prog_jezikov:
		if language['name'].startswith(izbrani_prog_jezik):
			id_prog_jezika = language['id']
			break

	naloga = 'Naloga 1'
	dobiInputeNaloge = core.utils.extract_cases(naloga, 'Input')

	url = "https://judge0-ce.p.rapidapi.com/submissions/batch"

	querystring = {"base64_encoded": "True", "fields": "*"}

	payload = {"submissions": [
		{
			"language_id": id_prog_jezika,
			"source_code": code,
			"stdin": dobiInputeNaloge[0]
		},
		{
			"language_id": id_prog_jezika,
			"source_code": code,
			"stdin": dobiInputeNaloge[1]
		},
		{
			"language_id": id_prog_jezika,
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
			tokens = []

			for response in response_data:
				tokens.append(response['token'])
			token_string_list = ','.join(tokens)
			# če grem na 3 sekunde, dobim vsake tolk časa status processing ali pa queued na submissions:(
			time.sleep(4)
			results = getBatchedSubmission(token_string_list)

			return results
		else:
			print("Failed to create submission.")

	except requests.exceptions.RequestException as e:
		print("Pojavila se je napaka:", str(e))


def getBatchedSubmission(tokens):
	print('--------------------------------------------------get batched submission')
	url = "https://judge0-ce.p.rapidapi.com/submissions/batch"

	querystring = {
		"tokens": tokens,
		"base64_encoded": "True", "fields": "*"}

	headers = {
		"X-RapidAPI-Key": X_RAPIDAPI_KEY,
		"X-RapidAPI-Host": X_RAPIDAPI_HOST
	}

	try:
		response = requests.get(url, headers=headers, params=querystring)
		response.raise_for_status()
		response_data = response.json()
		print(response_data, 'res')
		code_outputs = []

		for submission in response_data['submissions']:
			if submission['stdout']:
				outputs = ''.join(submission['stdout'])
				code_outputs.append(outputs)
			elif submission['stderr']:
				stderr = submission['stderr']
				raise Exception(stderr)
			# če ni stout in ne stderr potem se koda še obdeluje
			else:
				status = submission["status"]
				status_id = status["id"]
				description = status["description"]
				print("Status ID:", status_id)
				print("Description:", description)
		return code_outputs
	# če uspešno dobimo nazaj outpute
	except requests.exceptions.RequestException as e:
		print("Pojavila se je napaka:", str(e))

