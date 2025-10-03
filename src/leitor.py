from pypdf import PdfReader
from pathlib import Path
import re
import logging
import datetime

def ler_pdf(input_path: Path):
    file_list: list[Path] = []
    text_list: list[str] = []
    if not input_path.exists() or not input_path.is_dir():
        logging.error(f"O caminho {input_path} é inválido.")
        return file_list, text_list
    for file in input_path.glob('*.pdf'):
        file_list.append(file)
        with open(file, 'rb') as f:
            reader = PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            text_list.append(text)
    return file_list, text_list

def is_fatura_equatorial(text: str) -> bool:
    if re.search(r"Equatorial", text, re.IGNORECASE):
        return True
    return False
def extrair_fatura_equatorial(text:str,file_name:str,dados_anterior:dict= {"codigo_instalacao": [], "codigo_cliente": [], "periodo_referencia": [], "arquivo": [], "energia_consumida": [], "energia_compensada": [], "energia_faturada": [], "tarifa_sem_imposto": [], "icms": [], "pis": [], "cofins": [], "valor_total": [], "tipo_fornecimento": []}) -> dict:
    dados_anterior['arquivo'].append(file_name)
    regex_codigo_inst = re.compile(r"INSTALAÇÃO:\s*(\d+)", re.IGNORECASE)
    regex_codigo_cliente = re.compile(r"Conta Contrato\s+(\d+)", re.IGNORECASE)
    regex_mes_ref = re.compile(r"Conta M[eê]s\s+(\d{2})\/(\d{4})", re.MULTILINE)
    regex_energia_compensada = re.compile(r"Consumo\s+Compensado\s+\(kWh\)\s+((?:\d+\.)*\d+(?:,\d+)?)", re.IGNORECASE)
    regex_energia_faturada = re.compile(r"Consumo\s+\(kWh\)\s+((?:\d+\.)*\d+(?:,\d+)?)\s+\d\,\d+\s+(\d\,\d+)", re.IGNORECASE)
    regex_icms = re.compile(r"ICMS\s+(?:\d+\.)*\d+(?:,\d+)?\s+(\d+,\d+)", re.IGNORECASE)
    regex_pis = re.compile(r"PIS\s+(?:\d+\.)*\d+(?:,\d+)?\s+(\d+,\d+)", re.IGNORECASE)
    regex_cofins = re.compile(r"COFINS\s+(?:\d+\.)*\d+(?:,\d+)?\s+(\d+,\d+)", re.IGNORECASE)
    regex_valor_total = re.compile(r"Total\s+a\s+Pagar\s+R\$\s+((?:\d+\.)*\d+(?:,\d+)?)", re.MULTILINE)
    regex_tipo_fornecimento = re.compile(r"Tipo\s+de\s+Fornecimento:\s+(\w+)", re.IGNORECASE)
   
    # Match do código de instalação.
    match_codigo_inst = re.search(regex_codigo_inst, text)
    if match_codigo_inst:
        codigo_instalacao = int(match_codigo_inst.group(1))
        dados_anterior['codigo_instalacao'].append(codigo_instalacao)
        logging.info(f"Código de instalação encontrado: {codigo_instalacao}")
    else:
        dados_anterior['codigo_instalacao'].append(None)
        logging.warning("Nenhum código de instalação encontrado.")
    # Match do código do cliente.
    match_codigo_cliente = re.search(regex_codigo_cliente, text)
    if match_codigo_cliente:
        codigo_cliente = int(match_codigo_cliente.group(1))
        dados_anterior['codigo_cliente'].append(codigo_cliente)
        logging.info(f"Código de cliente encontrado: {codigo_cliente}")
    else:
        dados_anterior['codigo_cliente'].append(None)
        logging.warning("Nenhum código de cliente encontrado.")
    # Match da energia compensada.
    match_energia_compensada = re.search(regex_energia_compensada, text)
    if match_energia_compensada:
        energia_compensada = float(match_energia_compensada.group(1).replace('.','').replace(',','.'))
        logging.info(f"Energia compensada: {energia_compensada} kWh")
        dados_anterior['energia_compensada'].append(energia_compensada)
    else:
        energia_compensada = None
        dados_anterior['energia_compensada'].append(energia_compensada)
        logging.warning("Nenhuma energia compensada encontrada.")
    # Match da energia faturada.
    match_energia_faturada = re.search(regex_energia_faturada, text)
    if match_energia_faturada:
        energia_faturada = float(match_energia_faturada.group(1).replace('.','').replace(',','.'))
        tarifa_sem_imposto = float(match_energia_faturada.group(2).replace(',','.'))
        logging.info(f"Energia faturada: {energia_faturada} kWh")
        dados_anterior['energia_faturada'].append(energia_faturada)
        dados_anterior['tarifa_sem_imposto'].append(tarifa_sem_imposto)
    else:
        energia_faturada = None
        dados_anterior['energia_faturada'].append(energia_faturada)
        logging.warning("Nenhuma energia faturada encontrada.")
    # Cálculo da energia consumida.
    if energia_faturada is not None and energia_compensada is not None:
        energia_consumida = energia_faturada + energia_compensada
        logging.info(f"Energia consumida calculada: {energia_consumida} kWh")
    else:
        energia_consumida = None
        logging.warning("Não foi possível calcular a energia consumida.")
    dados_anterior['energia_consumida'].append(energia_consumida)
    # Match do período de referência.
    match_periodo_ref = re.search(regex_mes_ref, text)
    if match_periodo_ref:
        mes_ref_match = match_periodo_ref.group(1)
        ano_ref_match = match_periodo_ref.group(2)
        periodo_ref = datetime.datetime(int(ano_ref_match), int(mes_ref_match), 1)
    else:
        periodo_ref = None
        logging.warning("Nenhum período de referência encontrado.")
    dados_anterior['periodo_referencia'].append(periodo_ref)

    # Match do ICMS.
    match_icms = re.search(regex_icms, text)
    if match_icms:
        icms = float(match_icms.group(1).replace(',','.'))
    else:
        icms = None
        logging.warning("Nenhum valor de ICMS encontrado.")
    # Match do PIS.
    match_pis = re.search(regex_pis, text)
    if match_pis:
        pis = float(match_pis.group(1).replace(',','.'))
    else:
        pis = None
        logging.warning("Nenhum valor de PIS encontrado.")
    # Match do COFINS.
    match_cofins = re.search(regex_cofins, text)
    if match_cofins:
        cofins = float(match_cofins.group(1).replace(',','.'))
    else:
        cofins = None
        logging.warning("Nenhum valor de COFINS encontrado.")
    # Match do valor total.
    match_valor_total = re.search(regex_valor_total, text)
    if match_valor_total:
        valor_total = float(match_valor_total.group(1).replace('.','').replace(',','.'))
    else:
        valor_total = None
        logging.warning("Nenhum valor total encontrado.")
    # Match do tipo de fornecimento.
    match_tipo_fornecimento = re.search(regex_tipo_fornecimento, text)
    if match_tipo_fornecimento:
        tipo_fornecimento = match_tipo_fornecimento.group(1).upper()
    else:
        tipo_fornecimento = None
        logging.warning("Nenhum tipo de fornecimento encontrado.")
    # Adiciona os valores extraídos ao dicionário.
    dados_anterior['icms'].append(icms)
    dados_anterior['pis'].append(pis)
    dados_anterior['cofins'].append(cofins)
    dados_anterior['valor_total'].append(valor_total)
    dados_anterior['tipo_fornecimento'].append(tipo_fornecimento)

    logging.info(f"Dados extraídos do arquivo {file_name}")
    return dados_anterior