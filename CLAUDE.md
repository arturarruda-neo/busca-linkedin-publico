# CLAUDE.md — busca-linkedin

Automação que busca perfis LinkedIn de sócios de empresas em Google Sheets e preenche as colunas de contato.

## Planilha

- URL: `https://docs.google.com/spreadsheets/d/1jxZsQRlmF3OcznRc3z7o0xFhCbrGO-ADYUwpdwtpbyM/edit`
- Cabeçalho na linha 4 — dados das empresas começam na linha 5
- Coluna A é vazia; dados vão de B a P

| Coluna | Nome | Papel |
|--------|------|-------|
| C | Nome da Empresa | Usado na busca |
| K | Sócios | Lido — nomes separados por `\n` |
| L | Contato | **Escrito** — nome do sócio encontrado, ou "N.A." |
| O | LinkedIn | **Escrito** — URL, somente se a célula estiver vazia |

## Fluxo principal (WebSearch)

```bash
# 1. Ler dados da planilha
python "C:/secret-sauce/busca-linkedin/scripts/ler_planilha.py" "[URL]" [linha_inicial] [num_linhas]

# 2. Claude busca via WebSearch — query: {nome_sócio} {nome_empresa} LinkedIn
#    Coletar LinkedIn de TODOS os sócios com perfil (não apenas o primeiro)
#    Pular linhas onde coluna L já preenchida e diferente de "N.A."

# 3. Salvar resultados e atualizar planilha
python "C:/secret-sauce/busca-linkedin/scripts/atualizar_planilha.py" "[URL]" "C:/secret-sauce/busca-linkedin/output/resultados.json"
```

Formato do `resultados.json`:

```json
[
  {
    "linha": 17,
    "contatos": ["NOME A", "NOME B"],
    "urls_linkedin": ["https://linkedin.com/in/...", "https://linkedin.com/in/..."],
    "linkedin_existente": ""
  }
]
```

- `contatos` e `urls_linkedin` vazios → grava "N.A." em L e O
- Coluna O só é escrita se `linkedin_existente` estiver vazia

## Autenticação Google Sheets

- gspread OAuth Desktop
- Credenciais: `C:\Users\MF Capital\AppData\Roaming\gspread\credentials.json`
- Token expira ocasionalmente — reautenticar com:
  `& "C:\Users\MF Capital\AppData\Local\Python\pythoncore-3.14-64\python.exe" "C:\secret-sauce\busca-linkedin\scripts\autenticar_gspread.py"`

## Convenções

- Python 3, PEP 8
- Sem framework de testes
