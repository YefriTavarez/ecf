# Copyright (c) 2025, Yefri Tavarez and Contributors
# For license information, please see license.txt

import requests

settings = {
	"service_url": "https://signer.example.com",

}

# elements I need to sign
# username: str - User known by the signer service
# password: str - Password for the user
# client: str - Client ID to be used group the other elements (like a tag)
# p12: File - File containing the certificate to be used for signing
# p12_secret: str - Password for the p12 file
# p12_filepath: str - Path to the p12 file
# jwt_token: str - Token to be used after the login (upload the certificate, get a signed seed and sign the seed)
# bearer_token: str - Token to be used to authenticate the user for further requests
# service_url: str - URL for the signer
# xml_document: File - XML document to
# xml_docpath: str - Path to the XML document
# token_expiry: int - Time in seconds for the token to expire
# token_expires: datetime - Time when the token expires


# Worflow:
# 1. Authenticate the User (username, password and client)
# 2. Upload the certificate (p12, p12_secret and jwt_token)
# 3. Get a seed to sign (jwt_token)
# 4. Sign the seed (jwt_token and seed)
# 5. Get the signed document (jwt_token)
#



class eCFSignerClient:
	def __init__(self, settings):
		self.settings = settings

	def sign(self, xml_document: str):


"""
// Workflow
Get a token

curl -X POST http://ecf.tzcode.tech:3760/auth/login \
-H "Content-Type: application/json" \
-d '{"username": "usr_ciOiJIUzI", "password": "passwd_nR5cCI6IkpXVC", "client": "TzCode, S. R. L."}'
// Upload the certficate file

curl -X POST http://ecf.tzcode.tech:3760/upload-p12 \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRJZCI6IlR6Q29kZSwgUy4gUi4gTC4iLCJpYXQiOjE3NDEyNDE4OTYsImV4cCI6MTc0MTI4NTA5Nn0.bJ0ttDEdbaTQ0sXoORNf7twjL6jOTGYeUH56ByDR07A" \
-F "p12File=@/Users/freebird/Downloads/Firma Digital.p12" \
-F "secret=M@sterpass17.."



// Get a seed
curl -X 'GET' \
  'https://ecf.dgii.gov.do/CerteCF/Autenticacion/api/Autenticacion/Semilla' \
  -H 'Accept: text/xml' \
  -H 'Content-Type: text/xml'


// Sign the xml

curl -X POST http://ecf.tzcode.tech:3760/sign-xml \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRJZCI6IlR6Q29kZSwgUy4gUi4gTC4iLCJpYXQiOjE3NDEyNDE4OTYsImV4cCI6MTc0MTI4NTA5Nn0.bJ0ttDEdbaTQ0sXoORNf7twjL6jOTGYeUH56ByDR07A" \
-F "xmlFile=@/Users/freebird/Downloads/seed.xml"

// Renew the token
curl -X POST http://ecf.tzcode.tech:3760/auth/refresh \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRJZCI6IlR6Q29kZSwgUy4gUi4gTC4iLCJpYXQiOjE3NDEyNDE4OTYsImV4cCI6MTc0MTI4NTA5Nn0.bJ0ttDEdbaTQ0sXoORNf7twjL6jOTGYeUH56ByDR07A"

"""