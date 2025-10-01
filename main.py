from pathlib import Path
from src.leitor import ler_pdf, is_fatura_equatorial, extrair_fatura_equatorial
def main():
    input_path = Path("input")
    file_list, text_list = ler_pdf(input_path)
    for file, text in zip(file_list, text_list):
        if is_fatura_equatorial(text):
            dados = extrair_fatura_equatorial(text, file.name)
            print(dados)
        else:
            print(f"O arquivo {file.name} não é uma fatura da Equatorial.")
            continue


if __name__ == "__main__":
    main()
