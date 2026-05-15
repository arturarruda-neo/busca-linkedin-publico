# Organização do Projeto busca-linkedin — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Limpar estrutura de pastas e código do projeto busca-linkedin sem alterar comportamento.

**Architecture:** Série de edições cirúrgicas em arquivos existentes + criação de dois novos arquivos de configuração. Sem mudanças de lógica nos scripts Python.

**Tech Stack:** Python 3, gspread 6.x, google-auth-oauthlib — sem framework de testes.

> **Nota:** Este projeto não tem repositório git. Não há passos de commit.

---

### Task 1: Criar pasta `output/` e `.gitignore`

**Files:**
- Create: `C:/secret-sauce/busca-linkedin/output/.gitkeep`
- Create: `C:/secret-sauce/busca-linkedin/.gitignore`

- [ ] **Step 1: Criar pasta `output/` com arquivo sentinela**

```bash
mkdir -p /c/secret-sauce/busca-linkedin/output
touch /c/secret-sauce/busca-linkedin/output/.gitkeep
```

- [ ] **Step 2: Criar `.gitignore`**

Conteúdo exato do arquivo `C:/secret-sauce/busca-linkedin/.gitignore`:
```
output/resultados.json
```

- [ ] **Step 3: Verificar**

```bash
ls /c/secret-sauce/busca-linkedin/output/
ls /c/secret-sauce/busca-linkedin/.gitignore
```
Esperado: pasta `output/` existente com `.gitkeep`; arquivo `.gitignore` presente.

---

### Task 2: Criar `requirements.txt`

**Files:**
- Create: `C:/secret-sauce/busca-linkedin/requirements.txt`

- [ ] **Step 1: Criar `requirements.txt`**

Conteúdo exato:
```
gspread>=6.0.0
google-auth-oauthlib>=1.0.0
```

- [ ] **Step 2: Verificar que as versões instaladas são compatíveis**

```bash
python -c "import gspread; print(gspread.__version__)"
python -c "import google_auth_oauthlib; print('ok')"
```
Esperado: versão do gspread >= 6.0.0 impressa; "ok" para google-auth-oauthlib.

---

### Task 3: Limpar permissões obsoletas em `.claude/settings.local.json`

**Files:**
- Modify: `C:/secret-sauce/busca-linkedin/.claude/settings.local.json`

- [ ] **Step 1: Substituir conteúdo do arquivo**

Conteúdo exato após a edição:
```json
{
  "permissions": {
    "allow": [
      "Bash(python *)",
      "WebSearch"
    ]
  }
}
```

- [ ] **Step 2: Verificar JSON válido**

```bash
python -c "import json; json.load(open('/c/secret-sauce/busca-linkedin/.claude/settings.local.json'))" && echo "JSON válido"
```
Esperado: `JSON válido`

---

### Task 4: Remover comentários de QUÊ em `atualizar_planilha.py`

**Files:**
- Modify: `C:/secret-sauce/busca-linkedin/scripts/atualizar_planilha.py`

- [ ] **Step 1: Remover os dois comentários de QUÊ**

Conteúdo exato do arquivo após a edição:
```python
import sys
import json
import time
import gspread


def atualizar_planilha(url, arquivo_resultados):
    gc = gspread.oauth()
    sh = gc.open_by_url(url)
    ws = sh.get_worksheet(0)

    with open(arquivo_resultados, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    atualizacoes = []
    for r in resultados:
        linha = r["linha"]
        contato = r.get("contato", "N/A")
        url_linkedin = r.get("url_linkedin", "")
        email_existente = r.get("email_existente", "")

        atualizacoes.append({
            "range": f"K{linha}",
            "values": [[contato]],
        })

        if url_linkedin and not email_existente.strip():
            atualizacoes.append({
                "range": f"M{linha}",
                "values": [[url_linkedin]],
            })

    if atualizacoes:
        ws.batch_update(atualizacoes)
        time.sleep(1)  # respeitar rate limit da API

    encontrados = sum(1 for r in resultados if r.get("url_linkedin"))
    nao_encontrados = sum(1 for r in resultados if not r.get("url_linkedin"))
    email_ja_preenchido = sum(
        1 for r in resultados
        if r.get("url_linkedin") and r.get("email_existente", "").strip()
    )

    print(f"\nProcessamento concluído!")
    print(f"Total de linhas:         {len(resultados)}")
    print(f"✓ LinkedIn encontrado:   {encontrados}")
    print(f"✗ Não encontrado (N/A):  {nao_encontrados}")
    if email_ja_preenchido:
        print(f"~ E-mail já preenchido:  {email_ja_preenchido} (URL do LinkedIn não salva)")
    print(f"\nPlanilha atualizada com sucesso.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python atualizar_planilha.py <URL> <resultados.json>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    arquivo = sys.argv[2]
    atualizar_planilha(url, arquivo)
```

- [ ] **Step 2: Verificar sintaxe Python**

```bash
python -m py_compile /c/secret-sauce/busca-linkedin/scripts/atualizar_planilha.py && echo "Sintaxe ok"
```
Esperado: `Sintaxe ok`

---

### Task 5: Atualizar SKILL.md global — corrigir caminhos e path do resultados.json

**Files:**
- Modify: `C:/Users/MF Capital/.claude/plugins/busca-linkedin/skills/busca-linkedin/SKILL.md`

Três substituições no arquivo:

- [ ] **Step 1: Corrigir caminho do `ler_planilha.py` (Passo 3)**

Localizar:
```
python "C:/Users/MF Capital/.claude/plugins/busca-linkedin/skills/busca-linkedin/scripts/ler_planilha.py" "[URL]" [linha_inicial] [num_linhas]
```
Substituir por:
```
python "C:/secret-sauce/busca-linkedin/scripts/ler_planilha.py" "[URL]" [linha_inicial] [num_linhas]
```

- [ ] **Step 2: Corrigir path do `resultados.json` e caminho do `atualizar_planilha.py` (Passo 5)**

Localizar:
```
Salve como `resultados.json` na pasta do projeto e execute:

```bash
python "C:/Users/MF Capital/.claude/plugins/busca-linkedin/skills/busca-linkedin/scripts/atualizar_planilha.py" "[URL]" resultados.json
```
```
Substituir por:
```
Salve como `output/resultados.json` na pasta do projeto e execute:

```bash
python "C:/secret-sauce/busca-linkedin/scripts/atualizar_planilha.py" "[URL]" output/resultados.json
```
```

- [ ] **Step 3: Verificar que não há mais referências ao diretório de plugins nos comandos bash**

```bash
grep -n "plugins/busca-linkedin" "/c/Users/MF Capital/.claude/plugins/busca-linkedin/skills/busca-linkedin/SKILL.md"
```
Esperado: nenhuma linha retornada.

---

### Task 6: Remover `SKILL.md` do projeto e atualizar `CLAUDE.md`

**Files:**
- Delete: `C:/secret-sauce/busca-linkedin/SKILL.md`
- Modify: `C:/secret-sauce/busca-linkedin/CLAUDE.md`

- [ ] **Step 1: Remover `SKILL.md` do projeto**

```bash
rm /c/secret-sauce/busca-linkedin/SKILL.md
```

- [ ] **Step 2: Atualizar seção "Arquivos da Skill" no `CLAUDE.md`**

Localizar o bloco:
```
## Arquivos da Skill

A skill está instalada em:
```
C:\Users\MF Capital\.claude\plugins\busca-linkedin\skills\busca-linkedin\
├── SKILL.md                       # Instruções para o Claude
└── scripts\
    ├── ler_planilha.py            # Lê linhas da planilha via gspread
    └── atualizar_planilha.py      # Escreve resultados em batch via gspread
```
```

Substituir por:
```
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
```

- [ ] **Step 3: Atualizar seção "Estrutura do Repositório" no `CLAUDE.md`**

Localizar:
```
busca-linkedin/
├── CLAUDE.md                  # Este arquivo
├── SKILL.md                   # Instruções da skill para o Claude
├── scripts/
│   ├── ler_planilha.py        # Lê linhas da planilha via gspread
│   └── atualizar_planilha.py  # Escreve resultados em batch via gspread
└── resultados.json            # Gerado durante execução da skill (temporário)
```

Substituir por:
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

- [ ] **Step 4: Verificar estrutura final do projeto**

```bash
find /c/secret-sauce/busca-linkedin -not -path "*/docs/*" | sort
```
Esperado:
```
/c/secret-sauce/busca-linkedin
/c/secret-sauce/busca-linkedin/.claude
/c/secret-sauce/busca-linkedin/.claude/settings.local.json
/c/secret-sauce/busca-linkedin/.gitignore
/c/secret-sauce/busca-linkedin/CLAUDE.md
/c/secret-sauce/busca-linkedin/output
/c/secret-sauce/busca-linkedin/output/.gitkeep
/c/secret-sauce/busca-linkedin/requirements.txt
/c/secret-sauce/busca-linkedin/scripts
/c/secret-sauce/busca-linkedin/scripts/atualizar_planilha.py
/c/secret-sauce/busca-linkedin/scripts/ler_planilha.py
```
