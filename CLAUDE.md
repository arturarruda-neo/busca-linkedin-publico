# CLAUDE.md — Guia de Contexto do Projeto

## Visão Geral

Projeto **busca-linkedin**, parte da suite **secret-sauce**.
Automação para buscar perfis do LinkedIn de sócios de empresas listadas em uma planilha Google Sheets, preenchendo automaticamente as colunas de contato.

## Sobre o Projeto

O usuário possui uma planilha Google Sheets com centenas de empresas. Para cada empresa, a planilha lista os sócios. O objetivo é encontrar o perfil LinkedIn de pelo menos um sócio por empresa e registrar o nome do sócio encontrado e a URL do LinkedIn diretamente na planilha.

A busca é feita via Google (WebSearch), sócio por sócio, e a planilha é atualizada via API do Google Sheets (biblioteca gspread).

## Estrutura da Planilha (fixa — 15 colunas)

| Coluna | Nome | Papel |
|--------|------|-------|
| A | # | Identificador |
| B | Nome da Empresa | Usado na busca |
| C | Segmento | — |
| D | Cidade/UF | — |
| E | Razão Social | — |
| F | CNPJ | — |
| G | Receita Líquida | — |
| H | EBITDA | — |
| I | Margem EBITDA | — |
| J | Sócios | Lido — nomes separados por `\n` (Alt+Enter) |
| K | Contato | **Escrito** — nome do sócio encontrado, ou "N/A" |
| L | Telefone | — |
| M | E-mail | — |
| N | LinkedIn | **Escrito** — URL do LinkedIn, somente se a célula estiver vazia |
| O | Website | — |

## Lógica de Busca

1. Cabeçalho na linha 4 — dados das empresas começam na linha 5
2. Para cada linha (empresa), separar sócios da coluna J por `\n`
3. Para cada sócio (em ordem): WebSearch `[nome sócio] [nome empresa] linkedin`
4. Analisar os 4 primeiros resultados buscando URL `linkedin.com/in/...`
5. Primeiro match encontrado → preencher K (nome) e N (URL) e parar
6. Se nenhum sócio tiver match → preencher K com "N/A", não alterar N
7. Nunca sobrescrever a coluna N se já houver conteúdo

## Arquivos da Skill

A skill está instalada em:
```
C:\Users\MF Capital\.claude\plugins\busca-linkedin\skills\busca-linkedin\SKILL.md
```

Os scripts canônicos ficam no projeto:
```
C:\secret-sauce\busca-linkedin\scripts\
├── ler_planilha.py        # Lê linhas da planilha via gspread
└── atualizar_planilha.py  # Escreve resultados em batch via gspread
```

## Autenticação Google Sheets

- Biblioteca: `gspread` + `google-auth-oauthlib`
- Credenciais OAuth em: `C:\Users\MF Capital\AppData\Roaming\gspread\credentials.json`
  - **Atenção:** no Windows o gspread usa `AppData\Roaming\gspread\`, não `~/.config/gspread/`
- Usuário de teste autorizado na tela de consentimento OAuth: `arturdearrudacampos@gmail.com`
- Autenticação já realizada — token salvo localmente, não precisa autenticar novamente

## Regras de Interação

- Responda sempre em **português brasileiro**.
- Seja conciso e direto.
- Prefira editar arquivos existentes a criar novos.
- Não adicione comentários óbvios no código — apenas comente o **porquê** quando não for evidente.
- Não refatore além do escopo da tarefa solicitada.
- Não faça push nem alterações destrutivas sem confirmação explícita.

## Convenções de Código

- Linguagem: Python 3
- Estilo: PEP 8
- Scripts standalone — sem framework de testes por enquanto

## Estrutura do Repositório

```
busca-linkedin/
├── .claude/
│   └── settings.local.json
├── .gitignore
├── CLAUDE.md
├── requirements.txt
├── output/                    # Artefatos de execução (não versionados)
│   └── resultados.json        # Gerado durante execução da skill
└── scripts/
    ├── ler_planilha.py
    └── atualizar_planilha.py
```

## Planilha

- URL: `https://docs.google.com/spreadsheets/d/1jxZsQRlmF3OcznRc3z7o0xFhCbrGO-ADYUwpdwtpbyM/edit`
- Cabeçalho na linha 4 — dados das empresas começam na **linha 5**

## Estado do Setup (2026-04-23)

- [x] Skill criada e instalada
- [x] Python 3.14.4 instalado e disponível no PATH (`python --version` funciona direto no bash)
- [x] gspread 6.2.1 instalado
- [x] Credenciais Google Cloud criadas e autenticadas (OAuth Desktop, usuário de teste adicionado)
