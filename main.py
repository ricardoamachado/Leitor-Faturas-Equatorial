from pathlib import Path
from sys import argv
from src.leitor import ler_pdf, is_fatura_equatorial, extrair_fatura_equatorial
import pandas as pd
import logging
def main():
    export_type:str = argv[1] if len(argv) > 1 else "csv"
    input_str:str = argv[2] if len(argv) > 2 else "input"
    output_str:str = argv[3] if len(argv) > 3 else "output"
    if export_type.lower() not in ["csv", "excel"]:
        logging.error("Tipo de exportação inválido. Use 'csv' ou 'excel'.")
        return

    logging.basicConfig(level=logging.INFO)
    input_path = Path(input_str)
    output_path = Path(output_str)
    # Verifica se a entrada existe.
    if not input_path.exists():
        logging.error(f"O caminho {input_path} não existe.")
        return
    # Cria o diretório de saída se não existir.
    output_path.mkdir(parents=True, exist_ok=True)
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
    if export_type.lower() == "csv":
        output_file = output_path / f"faturas_equatorial_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        dados.to_csv(output_file, sep=';', decimal=',', encoding='utf-8')
    else:
        output_file = output_path / f"faturas_equatorial_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        dados.to_excel(output_file)
    logging.info(f"Dados exportados para {output_file}")

if __name__ == "__main__":
    main()
