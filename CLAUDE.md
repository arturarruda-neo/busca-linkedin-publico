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

## Script principal

```bash
python "C:/secret-sauce/busca-linkedin/scripts/buscar_linkedin_cse.py" "[URL]" [linha_inicial] [num_linhas]
```

Lê a planilha, busca LinkedIn via Google CSE (5 em paralelo), escreve L e O via batch_update.
Pula linhas com L já preenchido (diferente de vazio e "N.A.").

Requer: `GOOGLE_CSE_API_KEY` e `GOOGLE_CSE_ID` como variáveis de ambiente.
Cota CSE: 100 queries/dia gratuitas (~$5/1.000 além disso).

`ler_planilha.py` e `atualizar_planilha.py` são legados — usar só se o CSE falhar.

## Autenticação Google Sheets

- gspread OAuth Desktop
- Credenciais: `C:\Users\MF Capital\AppData\Roaming\gspread\credentials.json`
- Token já salvo — sem necessidade de nova autenticação

## Convenções

- Python 3, PEP 8
- Sem framework de testes
