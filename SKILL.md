---
name: busca-linkedin
description: Busca perfis do LinkedIn de sócios de empresas em uma planilha Google Sheets e preenche automaticamente as colunas de "Contato" e "LinkedIn". Use este skill sempre que o usuário pedir para buscar perfis no LinkedIn, encontrar sócios no LinkedIn, preencher URLs do LinkedIn em uma planilha, automatizar busca de contatos no LinkedIn, ou qualquer variação de "buscar linkedin de sócios/empresas/contatos".
---

# Busca de Perfis LinkedIn — Google Sheets

## Passo 1 — Confirmar configuração da planilha

Pergunte ao usuário (se não informado):

1. **URL** da planilha Google Sheets
2. **Linha inicial** dos dados (primeira linha após o cabeçalho)
3. **Quantas linhas** processar
4. **Mapeamento de colunas** — informe os padrões abaixo e pergunte se o usuário quer alterar:

| Parâmetro        | Padrão | Descrição                                          |
|------------------|--------|----------------------------------------------------|
| `--col-empresa`  | `C`    | Coluna com o nome da empresa                       |
| `--col-socios`   | `K`    | Coluna com os sócios (separados por quebra de linha) |
| `--col-contato`  | `L`    | Coluna onde gravar o nome do sócio encontrado      |
| `--col-linkedin` | `O`    | Coluna onde gravar a URL do LinkedIn               |

---

## Passo 2 — Ler a planilha

```bash
python scripts/ler_planilha.py "[URL]" [linha_inicial] [num_linhas] \
  --col-empresa [COL] --col-socios [COL] --col-contato [COL] --col-linkedin [COL]
```

O script imprime um JSON com a lista de empresas, sócios, contato atual e LinkedIn existente.

**Pule** linhas onde `contato` já está preenchido e é diferente de `"N.A."`.

---

## Passo 3 — Buscar LinkedIn via WebSearch

Dispare todas as buscas **em paralelo** — uma chamada WebSearch por sócio, em uma única mensagem com múltiplos tool calls.

Para cada sócio a buscar:

- Query: `{nome_sócio} {nome_empresa} LinkedIn`
- Parâmetro: `allowed_domains: ["linkedin.com"]` — obrigatório em todas as chamadas
- Critério de match: resultado com URL contendo `linkedin.com/in/`
- Colete LinkedIn de **todos** os sócios que tiverem perfil encontrado
- Se nenhum sócio tiver perfil, a lista fica vazia (será gravado "N.A.")

---

## Passo 4 — Montar o JSON de resultados

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

## Passo 5 — Atualizar a planilha

```bash
python scripts/atualizar_planilha.py "[URL]" "output/resultados.json" \
  --col-contato [COL] --col-linkedin [COL]
```

O script grava a coluna de contato para todas as linhas processadas e a coluna de LinkedIn apenas se a célula estiver vazia.
