# Copyright (c) 2025, Yefri Tavarez and Contributors
# For license information, please see license.txt

import io
import requests
import frappe

from frappe import (
    _dict as dictify,
    # enqueue as enqueue_job,
)


# sample_settings = dictify({
# 	"service_url": "ecf.example.com",
# 	"scheme": ["http" | "https"],
# 	"port": 6767,
# 	"username": "username",
# 	"password": "password",
# 	"client": "ABC, S. R. L.",
# })


def get_settings():
    """
    Obtiene la configuración de la aplicación ECF desde el sistema.
    """
    settings = frappe.get_single("ECF Settings")

    return dictify({
        "service_url": settings.signer_url,
        "scheme": settings.scheme,
        "port": settings.port,
        "username": settings.signer_user,
        "password": settings.get_password("signer_password"),
        "client": settings.company
    })

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

    def sign_xml(self, seed: str, tag_name: str=None):
        conf = self.settings

        url = f"{conf.scheme}://{conf.service_url}:{conf.port}/sign-xml"
        headers = {
            "Authorization": f"Bearer {self.jwt_token}"
        }

        # seedpath = f"/tmp/{self.jwt_token}.xml"
        # with open(seedpath, "w") as f:
            # f.write(seed)

        file_bytes = io.BytesIO(seed.encode('utf-8'))
        file_bytes.name = '{self.jwt_token}.xml'  # Set the filename for the BytesIO object

        files = {
            # "xmlFile": open(seedpath, "rb"),
            "xmlFile": (file_bytes.name, file_bytes, 'application/xml'),
        }

        if tag_name:
            data = {
                "tagName": tag_name,
            }
        else:
            data = {}
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        # files["xmlFile"].close()
        
        # Enqueue a job to remove the seed file after signing
        # enqueue_job(
        #     method=remove_seed,
        #     queue="default",
        #     timeout=300,
        #     job_name=f"Remove Seed {seedpath}",
        #     seedpath=seedpath,
        # )

        return response.text

    def json_to_xml(self, json_data: dict) -> str:
        """
        Convierte un diccionario de Python a XML utilizando el endpoint /json-to-xml del servidor.

        Args:
            json_data (dict): El diccionario de Python a convertir.

        Returns:
            str: La representación XML de los datos JSON.

        Raises:
            requests.exceptions.HTTPError: Si la petición al servidor falla.
        """
        conf = self.settings
        url = f"{conf.scheme}://{conf.service_url}:{conf.port}/json-to-xml"
        headers = {
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()
        return response.text

    def send_signed_invoice(self, signed_xml_filepath: str, invoice_type: str = None):
        """
        Envía el archivo XML firmado al endpoint /send-invoice del servidor.

        Args:
            signed_xml_filepath (str): La ruta al archivo XML que ya ha sido firmado.
            invoice_type (str, optional): El tipo de factura (ej: 'FC_MENOR_250K'). Defaults to None.
        """
        conf = self.settings
        url = f"{conf.scheme}://{conf.service_url}:{conf.port}/send-invoice"
        headers = {
            "Authorization": f"Bearer {self.jwt_token}"
        }
        files = {
            "signedXmlFile": open(signed_xml_filepath, "rb"),
        }
        data = {}
        if invoice_type:
            data["invoiceType"] = invoice_type

        try:
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            return response.json()  # O response.text si el servidor responde con texto
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar la factura: {e}")
            if response is not None:
                print(f"Respuesta del servidor: {response.status_code} - {response.text}")
            return None



def remove_seed(seedpath):
    import os
    os.remove(seedpath)
    return seedpath
