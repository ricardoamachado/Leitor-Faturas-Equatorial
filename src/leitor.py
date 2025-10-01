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
def extrair_fatura_equatorial(text:str,file_name:str) -> dict:
    dados = {}
    dados['arquivo'] = file_name
    regex_codigo_inst = re.compile(r"INSTALAÇÃO:\s*(\d+)", re.IGNORECASE)
    regex_codigo_cliente = re.compile(r"Conta Contrato\s+(\d+)", re.IGNORECASE)
    regex_mes_ref = re.compile(r"Conta M[eê]s\s+(\d{2})\/(\d{4})", re.MULTILINE)
    dados ['codigo_instalacao'] = re.search(regex_codigo_inst, text).group(1) if re.search(regex_codigo_inst, text) else None
    dados ['codigo_cliente'] = re.search(regex_codigo_cliente, text).group(1) if re.search(regex_codigo_cliente, text) else None
    mes_ref_match = re.search(regex_mes_ref, text).group(1)
    ano_ref_match = re.search(regex_mes_ref, text).group(2)
    periodo_ref = datetime.datetime(int(ano_ref_match), int(mes_ref_match), 1)
    dados ['periodo_referencia'] = periodo_ref
    logging.info(f"Dados extraídos do arquivo {file_name}: {dados}")
    return dados