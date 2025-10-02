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
def extrair_fatura_equatorial(text:str,file_name:str,dados_anterior:dict= {"codigo_instalacao": [], "codigo_cliente": [], "periodo_referencia": [], "arquivo": [], "energia_compensada": [], "energia_faturada": []}) -> dict:
    dados_anterior['arquivo'].append(file_name)
    regex_codigo_inst = re.compile(r"INSTALAÇÃO:\s*(\d+)", re.IGNORECASE)
    regex_codigo_cliente = re.compile(r"Conta Contrato\s+(\d+)", re.IGNORECASE)
    regex_mes_ref = re.compile(r"Conta M[eê]s\s+(\d{2})\/(\d{4})", re.MULTILINE)
    regex_energia_compensada = re.compile(r"Consumo\s+Compensado\s+\(kWh\)\s+((?:\d+\.)*\d+(?:,\d+)?)", re.IGNORECASE)
    regex_energia_faturada = re.compile(r"Consumo\s+\(kWh\)\s+((?:\d+\.)*\d+(?:,\d+)?)", re.IGNORECASE)
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
        logging.info(f"Energia faturada: {energia_faturada} kWh")
        dados_anterior['energia_faturada'].append(energia_faturada)
    else:
        energia_faturada = None
        dados_anterior['energia_faturada'].append(energia_faturada)
        logging.warning("Nenhuma energia faturada encontrada.")
    # Match do período de referência.
    mes_ref_match = re.search(regex_mes_ref, text).group(1)
    ano_ref_match = re.search(regex_mes_ref, text).group(2)
    periodo_ref = datetime.datetime(int(ano_ref_match), int(mes_ref_match), 1)
    dados_anterior['periodo_referencia'].append(periodo_ref)
    logging.info(f"Dados extraídos do arquivo {file_name}")
    return dados_anterior