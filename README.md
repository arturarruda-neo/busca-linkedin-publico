# busca-linkedin

Skill para [Claude Code](https://claude.ai/code) que automatiza a busca de perfis LinkedIn de sócios de empresas em uma planilha Google Sheets.

## Como funciona

1. Claude lê os dados da planilha via `scripts/ler_planilha.py`
2. Busca perfis LinkedIn via WebSearch (sem API externa, sem custo adicional)
3. Grava os resultados de volta na planilha via `scripts/atualizar_planilha.py`

## Pré-requisitos

- Python 3.8+
- Conta Google com acesso ao [Google Cloud Console](https://console.cloud.google.com)
- Claude Code com WebSearch habilitado

## Instalação

```bash
git clone https://github.com/arturarruda-neo/busca-linkedin-publico.git
cd busca-linkedin-publico
pip install -r requirements.txt
```

## Configuração do Google Sheets

### 1. Criar credenciais OAuth no Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com)
2. Crie um projeto (ou use um existente)
3. Ative a **Google Sheets API** e a **Google Drive API**
4. Vá em **APIs & Services → Credentials → Create Credentials → OAuth client ID**
5. Selecione o tipo **Desktop app**
6. Baixe o arquivo JSON gerado e salve em:
   - **Windows:** `%APPDATA%\gspread\credentials.json`
   - **Linux/Mac:** `~/.config/gspread/credentials.json`

### 2. Autenticar

```bash
python scripts/autenticar_gspread.py
```

Copie a URL exibida no terminal e abra no navegador para completar a autenticação OAuth. O token será salvo automaticamente.

## Estrutura esperada da planilha

A planilha deve ter colunas para: nome da empresa, sócios (um por linha dentro da célula), e duas colunas de saída (contato encontrado e URL do LinkedIn).

**Colunas padrão:**

| Coluna | Conteúdo |
|--------|----------|
| C | Nome da empresa |
| K | Nomes dos sócios (um por linha) |
| L | **Saída:** nome do sócio encontrado (ou "N.A.") |
| O | **Saída:** URL do LinkedIn (ou "N.A.") |

As colunas são totalmente configuráveis — veja [Configuração de colunas](#configuração-de-colunas).

## Instalação do Skill no Claude Code

Copie o `SKILL.md` para o diretório de skills do Claude Code:

```bash
# Windows
copy SKILL.md "%USERPROFILE%\.claude\skills\busca-linkedin.md"

# Linux/Mac
cp SKILL.md ~/.claude/skills/busca-linkedin.md
```

Reinicie o Claude Code. O skill estará disponível como `/busca-linkedin`.

## Uso

No Claude Code, invoque o skill:

```
/busca-linkedin
```

O skill irá confirmar:
- URL da planilha
- Linha inicial dos dados
- Quantas linhas processar
- Mapeamento de colunas (se diferente do padrão)

## Configuração de colunas

Se a sua planilha tem uma estrutura diferente, informe as colunas ao usar o skill ou passe diretamente nos scripts:

```bash
python scripts/ler_planilha.py "URL_DA_PLANILHA" 5 20 \
  --col-empresa B \
  --col-socios F \
  --col-contato G \
  --col-linkedin H
```

```bash
python scripts/atualizar_planilha.py "URL_DA_PLANILHA" output/resultados.json \
  --col-contato G \
  --col-linkedin H
```

## Segurança

- O arquivo `.env` é gitignored — nunca commite credenciais
- As credenciais OAuth ficam apenas localmente (`%APPDATA%\gspread\` ou `~/.config/gspread/`)
- O arquivo `output/resultados.json` é gitignored — pode conter dados pessoais
