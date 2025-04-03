from datetime import datetime

def generar_xml_e31(datos_encabezado, detalles_items, firma_digital):
    """
    Genera el XML para una Factura de Crédito Fiscal Electrónica (E31) con los campos obligatorios.

    Args:
        datos_encabezado (dict): Diccionario con los datos del encabezado.
        detalles_items (list): Lista de diccionarios, donde cada diccionario representa un ítem del detalle.
        firma_digital (str): La cadena de la firma digital.

    Returns:
        str: El XML generado.
    """
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<eCF>
    <Encabezado>
        <IdDoc>
            <TipoeCF>{datos_encabezado['TipoeCF']}</TipoeCF>
        </IdDoc>
        <Emisor>
            <RncEmisor>{datos_encabezado['RncEmisor']}</RncEmisor>
            <NombreEmisor>{datos_encabezado['NombreEmisor']}</NombreEmisor>
            <DireccionEmisor>{datos_encabezado['DireccionEmisor']}</DireccionEmisor>
            <Municipio>{datos_encabezado['Municipio']}</Municipio>
            <Provincia>{datos_encabezado['Provincia']}</Provincia>
            <FechaEmision>{datos_encabezado['FechaEmision']}</FechaEmision>
        </Emisor>
        <Comprador>
            <RNCComprador>{datos_encabezado['RNCComprador']}</RNCComprador>
            <NombreComprador>{datos_encabezado['NombreComprador']}</NombreComprador>
        </Comprador>
        <Totales>
            <SubTotalMontoGravadoI1>{datos_encabezado['SubTotalMontoGravadoI1']:.2f}</SubTotalMontoGravadoI1>
            <ITBIS1>{datos_encabezado['ITBIS1']:.2f}</ITBIS1>
            <TotalMontoFacturado>{datos_encabezado['TotalMontoFacturado']:.2f}</TotalMontoFacturado>
            <ValorPagar>{datos_encabezado['ValorPagar']:.2f}</ValorPagar>
        </Totales>
    </Encabezado>
    <Detalle>
    """
    for item in detalles_items:
        xml += f"""
        <Item>
            <NumeroLinea>{item['NumeroLinea']}</NumeroLinea>
            <IndicadorFacturacion>{item['IndicadorFacturacion']}</IndicadorFacturacion>
            <NombreItem>{item['NombreItem']}</NombreItem>
            <Cantidad>{item['Cantidad']:.2f}</Cantidad>
            <PrecioUnitarioItem>{item['PrecioUnitarioItem']:.2f}</PrecioUnitarioItem>
            <MontoItem>{item['MontoItem']:.2f}</MontoItem>
        </Item>
        """
    xml += """
    </Detalle>
    <FirmaDigital>
        <SignatureValue>"""
    xml += f"{firma_digital}"
    xml += """</SignatureValue>
    </FirmaDigital>
</eCF>"""
    return xml
