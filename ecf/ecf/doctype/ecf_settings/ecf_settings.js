// Copyright (c) 2025, TzCode, S. R. L. and contributors
// For license information, please see license.txt

{
	function environment(frm) {
		// TesteCF: Ambiente de pre-certificación:
		// https://ecf.dgii.gov.do/testecf/autenticacion
		//
		// CerteCF: Ambiente de certificación:
		// https://ecf.dgii.gov.do/certecf/autenticacion
		//
		// eCF: Ambiente de producción:
		// https://ecf.dgii.gov.do/ecf/autenticacion
		//
		
		const { doc } = frm;
		if (doc.environment === "TesteCF") {
			doc.service_url = "https://ecf.dgii.gov.do/testecf/autenticacion";
		} else if (doc.environment === "CerteCF") {
			doc.service_url = "https://ecf.dgii.gov.do/certecf/autenticacion";
		} else if (doc.environment === "eCF") {
			doc.service_url = "https://ecf.dgii.gov.do/ecf/autenticacion";
		} else {
			doc.service_url = "";
		}
		
		frm.refresh_field("service_url");
	}

	frappe.ui.form.on("ECF Settings", {
		environment,
	});
}
