# Copyright (c) 2025, Yefri Tavarez and Contributors
# For license information, please see license.txt

import requests

from frappe import (
	# _dict as dictify,
	enqueue as enqueue_job,
)


# sample_settings = dictify({
# 	"service_url": "ecf.example.com",
# 	"scheme": ["http" | "https"],
# 	"port": 6767,
# 	"username": "username",
# 	"password": "password",
# 	"client": "ABC, S. R. L.",
# })

class eCFSignerClient:
	def __init__(self, settings):
		self.settings = settings
		self.jwt_token = None
		self.authenticate_user()

	def authenticate_user(self):
		conf = self.settings

		url = f"{conf.scheme}://{conf.service_url}:{conf.port}/auth/login"

		payload = {
			"username": conf.username,
			"password": conf.password,
			"client": conf.client
		}
		response = requests.post(url, json=payload)
		response.raise_for_status()
		self.jwt_token = response.json().get("token")

	def upload_certificate(self, p12_filepath: str, p12_secret: str):
		conf = self.settings
		url = f"{conf.scheme}://{conf.service_url}:{conf.port}/upload-p12"
		headers = {
			"Authorization": f"Bearer {self.jwt_token}"
		}

		files = {
			"p12File": open(p12_filepath, "rb"),
		}

		data = {
			"secret": p12_secret,
		}

		response = requests.post(url, headers=headers, files=files, data=data)
		response.raise_for_status()

	def _get_seed(self):
		conf = self.settings

		url = f"{conf.scheme}://{conf.service_url}:{conf.port}/get-seed"
		headers = {
			"Authorization": f"Bearer {self.jwt_token}"
		}
		response = requests.get(url, headers=headers)
		response.raise_for_status()
		return response.text
	
	def get_seed(self):
		url = "https://ecf.dgii.gov.do/CerteCF/Autenticacion/api/Autenticacion/Semilla"
		headers = {
			"Accept": "text/xml",
			"Content-Type": "text/xml"
		}

		response = requests.get(url, headers=headers)
		response.raise_for_status()
		return response.text

		
	def get_signed_seed(self, path=None):
		seed = self.get_seed()
		signed_seed = self.sign_seed(seed)

		if path:
			with open(path, "w") as f:
				f.write(signed_seed)

			return path
 
		return signed_seed

	def sign_seed(self, seed: str):
		conf = self.settings

		url = f"{conf.scheme}://{conf.service_url}:{conf.port}/sign-xml"
		headers = {
			"Authorization": f"Bearer {self.jwt_token}"
		}

		seedpath = f"/tmp/{self.jwt_token}.xml"
		with open(seedpath, "w") as f:
			f.write(seed)

		files = {
			"xmlFile": open(seedpath, "rb"),
		}
		response = requests.post(url, headers=headers, files=files)
		response.raise_for_status()
		
		enqueue_job(
			method=remove_seed,
			queue="default",
			timeout=300,
			job_name=f"Remove Seed {seedpath}",
			seedpath=seedpath,
		)

		return response.text


def remove_seed(seedpath):
	import os
	os.remove(seedpath)
	return seedpath
