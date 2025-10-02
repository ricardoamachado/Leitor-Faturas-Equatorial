from pathlib import Path
from src.leitor import ler_pdf, is_fatura_equatorial, extrair_fatura_equatorial
import pandas as pd
import logging
def main():
    logging.basicConfig(level=logging.INFO)
    input_path = Path("input")
    file_list, text_list = ler_pdf(input_path)
    counter: int = 0
    for file, text in zip(file_list, text_list):
        if is_fatura_equatorial(text):
            if counter == 0:
                dados = extrair_fatura_equatorial(text, file.name)
                counter += 1
            else:
                dados = extrair_fatura_equatorial(text, file.name, dados)
        else:
            print(f"O arquivo {file.name} não é uma fatura da Equatorial.")
            continue
    dados = pd.DataFrame(dados)
    dados = dados.set_index(['codigo_instalacao', 'periodo_referencia'])
    print(dados)

if __name__ == "__main__":
    main()
