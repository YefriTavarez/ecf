# Copyright (c) 2025, Yefri Tavarez and Contributors
# For license information, please see license.txt

import frappe
import xml.etree.ElementTree as ET


def send_to_dgii(doc, method):
	...


def convert_invoice_to_xml(invoice):
    root = ET.Element("eCF")

    # Encabezado
    encabezado = ET.SubElement(root, "Encabezado")
    ET.SubElement(encabezado, "NCF").text = invoice.ncf
    ET.SubElement(encabezado, "FechaEmision").text = invoice.posting_date
    ET.SubElement(encabezado, "Moneda").text = invoice.currency
    ET.SubElement(encabezado, "TotalITBIS").text = str(invoice.total_taxes_and_charges)
    ET.SubElement(encabezado, "TotalFactura").text = str(invoice.grand_total)

    # Emisor (hardcoded)
    emisor = ET.SubElement(root, "Emisor")
    ET.SubElement(emisor, "RNC").text = invoice.company_tax_id
    ET.SubElement(emisor, "RazonSocial").text = invoice.company
    ET.SubElement(emisor, "Direccion").text = invoice.company_address_display

    # Receptor (cliente)
    receptor = ET.SubElement(root, "Receptor")
    ET.SubElement(receptor, "RNC").text = invoice.tax_id
    ET.SubElement(receptor, "RazonSocial").text = invoice.customer_name
    ET.SubElement(receptor, "Direccion").text = invoice.address_display

    # Detalle de productos
    detalle = ET.SubElement(root, "Detalle")
    for item in invoice.items:
        item_xml = ET.SubElement(detalle, "Item")
        ET.SubElement(item_xml, "Codigo").text = item["item_code"]
        ET.SubElement(item_xml, "Descripcion").text = item["description"]
        ET.SubElement(item_xml, "Cantidad").text = str(item["qty"])
        ET.SubElement(item_xml, "PrecioUnitario").text = str(item["rate"])
        ET.SubElement(item_xml, "Total").text = str(item["amount"])

    # Convertir a string
    return ET.tostring(root, encoding="utf-8", method="xml").decode()