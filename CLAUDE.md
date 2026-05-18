# CLAUDE.md — busca-linkedin

Automação que busca perfis LinkedIn de sócios de empresas em Google Sheets e preenche as colunas de contato.

## Estrutura do projeto

```
scripts/
  ler_planilha.py       # lê dados da planilha e imprime JSON
  atualizar_planilha.py # recebe resultados.json e atualiza a planilha
  autenticar_gspread.py # autenticação OAuth com Google Sheets
output/
  resultados.json       # gerado pelo fluxo — gitignored
.env                    # chaves de API opcionais — gitignored
SKILL.md                # skill do Claude Code para automação completa
```

## Fluxo principal

O skill `busca-linkedin` (definido em `SKILL.md`) gerencia o fluxo completo:

1. Lê dados com `ler_planilha.py`
2. Busca perfis via WebSearch
3. Salva `output/resultados.json`
4. Atualiza a planilha com `atualizar_planilha.py`

## Scripts

Todos os scripts aceitam parâmetros de colunas (`--col-empresa`, `--col-socios`, `--col-contato`, `--col-linkedin`) para funcionar com qualquer estrutura de planilha. Padrões: C, K, L, O.

## Autenticação Google Sheets

- gspread OAuth Desktop
- Credenciais em `%APPDATA%\gspread\` (Windows) ou `~/.config/gspread/` (Linux/Mac)
- Reautenticar: `python scripts/autenticar_gspread.py`

## Convenções

- Python 3, PEP 8
- Sem framework de testes
