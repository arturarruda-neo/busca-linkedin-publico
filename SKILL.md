---
name: busca-linkedin
description: Busca perfis do LinkedIn de sócios de empresas em uma planilha Google Sheets e preenche automaticamente as colunas de "Contato" e "LinkedIn". Use este skill sempre que o usuário pedir para buscar perfis no LinkedIn, encontrar sócios no LinkedIn, preencher URLs do LinkedIn em uma planilha, automatizar busca de contatos no LinkedIn, ou qualquer variação de "buscar linkedin de sócios/empresas/contatos".
---

# Busca de Perfis LinkedIn — Google Sheets

Automatiza a busca de perfis LinkedIn de sócios de empresas, lendo os dados de uma planilha Google Sheets e escrevendo os resultados nas colunas de contato e LinkedIn definidas pelo usuário.

---

## Passo 1 — Verificar configuração

Verifique se existem no diretório do projeto:
- `config/config.json` com as letras de coluna corretas para a planilha do usuário
- gspread OAuth2 configurado — requer `credentials.json` do Google Cloud Console
  (guia completo: https://docs.gspread.org/en/latest/oauth2.html e seção "Configuração do Google Sheets" no README)

Se as dependências não estiverem instaladas:
```bash
pip install -r requirements.txt
```

---

## Passo 2 — Configurar colunas

Pergunte ao usuário:

1. **Qual é a letra da coluna com o nome da empresa?** (ex: `A`)
2. **Qual é a letra da coluna com os sócios?** (um por linha dentro da célula, ex: `B`)
3. **Qual é a letra da coluna onde gravar o contato encontrado?** (ex: `C`)
4. **Qual é a letra da coluna onde gravar a URL do LinkedIn?** (ex: `D`)

Com as respostas, edite `config/config.json`:

```json
{
  "columns": {
    "empresa": "A",
    "socios": "B",
    "contato": "C",
    "linkedin": "D"
  }
}
```

---

## Passo 3 — Coletar informações da planilha

Pergunte ao usuário:

1. **URL da planilha** Google Sheets
2. **A partir de qual linha processar?** (primeira linha de dados, após o cabeçalho)
3. **Quantas linhas processar nessa rodada?**

Se o usuário informar "linha X até linha Y", calcular `num_linhas = Y - linha_inicial + 1`.

---

## Passo 4 — Ler a planilha

```bash
python scripts/ler_planilha.py "[URL]" [linha_inicial] [num_linhas]
```

O script lê as colunas definidas em `config/config.json` e imprime um JSON com empresas, sócios, contato atual e LinkedIn existente.

**Pule** linhas onde `contato` já está preenchido e é diferente de `"N.A."`.

---

## Passo 5 — Buscar LinkedIn via WebSearch

Dispare todas as buscas **em paralelo** — uma chamada WebSearch por sócio, em uma única mensagem com múltiplos tool calls.

Para cada sócio a buscar:

- Query: `{nome_sócio} {nome_empresa} LinkedIn`
- Parâmetro: `allowed_domains: ["linkedin.com"]` — obrigatório em todas as chamadas
- Critério de match: resultado com URL contendo `linkedin.com/in/`
- Colete LinkedIn de **todos** os sócios que tiverem perfil encontrado
- Se nenhum sócio tiver perfil, a lista fica vazia (será gravado "N.A.")

---

## Passo 6 — Montar o JSON de resultados

Construa uma lista com **apenas as empresas processadas** (não as puladas) neste formato:

```json
[
  {
    "linha": 17,
    "contatos": ["NOME SOCIO A", "NOME SOCIO B"],
    "urls_linkedin": ["https://www.linkedin.com/in/...", "https://www.linkedin.com/in/..."],
    "linkedin_existente": ""
  },
  {
    "linha": 18,
    "contatos": [],
    "urls_linkedin": [],
    "linkedin_existente": ""
  }
]
```

- `contatos` e `urls_linkedin` são listas paralelas (índice 0 corresponde ao índice 0)
- Listas vazias resultam em "N.A." na planilha
- Salve em `output/resultados.json`

---

## Passo 7 — Atualizar a planilha

```bash
python scripts/atualizar_planilha.py "[URL]" "output/resultados.json"
```

O script grava a coluna de contato para todas as linhas processadas e a coluna de LinkedIn apenas se a célula estiver vazia.

---

## Problemas comuns

| Problema | Solução |
|----------|---------|
| `SpreadsheetNotFound` | Verificar URL da planilha e permissão de acesso |
| `ModuleNotFoundError` | Rodar `pip install -r requirements.txt` |
| `python: command not found` | Usar `python3` no lugar de `python` (Mac/Linux) |
| `FileNotFoundError: credentials.json` | Seguir o guia de OAuth no README |
| Token expirado (erro 401) | Rodar `python scripts/autenticar_gspread.py` para reautenticar |
| Linhas já preenchidas não são reprocessadas | Regra de skip bloqueia qualquer contato diferente de "N.A."; limpar a célula para reprocessar |
