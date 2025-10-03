# Script para extrair informações da fatura de energia da Equatorial.

## Informações extraídas da fatura
O script extrai os seguintes dados das faturas de energia da Equatorial:

- Número do código de instalação
- Período de referência da fatura
- Número do código do cliente
- Nome do arquivo
- Energia consumida (kWh)
- Energia compensada (kWh)
- Energia faturada (kWh)
- Tarifa sem imposto (R$/kWh)
- Alíquota do ICMS (%)
- Alíquota do PIS (%)
- Alíquota do COFINS (%)
- Valor total da fatura (R$)
- Tipo de fornecimento: Monofásico, Bifásico ou Trifásico

## Requisitos

* Python 3.13 ou superior
* Gerenciador de pacotes uv - [link](https://docs.astral.sh/uv/getting-started/installation/)
* Dependências listadas no arquivo pyproject.toml

## Guia de utilização do script

1) Digite o comando abaixo no terminal para instalar os pacotes necessários para execução do script.

```
uv sync
```

2) Execute o script utilizando o comando abaixo, substituindo `<export_type>`, `<input_path>` e `<output_path>` pelos valores desejados:

```
uv run main.py <export_type> <input_path> <output_path>
```

- `<export_type>`: formato de exportação desejado (`csv` ou `excel`).
- `<input_path>`: caminho para os arquivos de entrada (faturas).
- `<output_path>`: caminho o arquivo de saída.

**Exemplo de uso:**

```
uv run main.py csv "input" "output"
```
