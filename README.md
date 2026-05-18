# busca-linkedin

Skill para [Claude Code](https://claude.ai/code) que busca automaticamente perfis LinkedIn de sócios de empresas em uma planilha Google Sheets e preenche as colunas de contato.

Desenvolvido como skill do Claude Code — pode ser acionado diretamente pelo Claude ou executado manualmente via linha de comando.

## O que faz

- Lê os nomes dos sócios e o nome da empresa das colunas configuradas na sua planilha
- Busca o perfil LinkedIn de cada sócio via WebSearch (sem custo adicional, sem API externa)
- Preenche as colunas de contato e URL do LinkedIn
- Pula linhas que já possuem contato preenchido (evita reprocessar)

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

Este projeto usa autenticação OAuth2 via [gspread](https://gspread.readthedocs.io). O processo exige criar credenciais no Google Cloud Console antes da primeira execução:

1. Acesse o [Google Cloud Console](https://console.cloud.google.com) e crie um projeto (ou use um existente)
2. Ative a **Google Sheets API** e a **Google Drive API** no projeto
3. Em **APIs e serviços > Credenciais**, crie uma credencial do tipo **ID do cliente OAuth 2.0** (tipo: aplicativo de área de trabalho)
4. Baixe o arquivo `credentials.json` gerado e salve em:
   - **Linux/Mac:** `~/.config/gspread/credentials.json`
   - **Windows:** `C:\Users\SEU_USUARIO\AppData\Roaming\gspread\credentials.json`
5. Execute o script de autenticação:

**Mac/Linux:**
```bash
python3 scripts/autenticar_gspread.py
```

**Windows:**
```cmd
python scripts\autenticar_gspread.py
```

Copie a URL exibida no terminal e abra no navegador para autorizar. O token será salvo automaticamente.

Para mais detalhes, consulte a [documentação oficial do gspread](https://docs.gspread.org/en/latest/oauth2.html).

## Estrutura esperada da planilha

A planilha deve ter colunas para: nome da empresa, sócios (um por linha dentro da célula) e duas colunas de saída (contato encontrado e URL do LinkedIn).

**Colunas padrão (configuráveis em `config/config.json`):**

| Coluna | Conteúdo |
|--------|----------|
| C | Nome da empresa |
| K | Nomes dos sócios (um por linha) |
| L | **Saída:** nome do sócio encontrado (ou "N.A.") |
| O | **Saída:** URL do LinkedIn (ou "N.A.") |

## Configuração das colunas

Antes de rodar, edite `config/config.json` com as letras das colunas da sua planilha:

```json
{
  "columns": {
    "empresa": "C",
    "socios": "K",
    "contato": "L",
    "linkedin": "O"
  }
}
```

> Os valores `C`, `K`, `L`, `O` são os padrões. Troque pelas letras correspondentes na sua planilha antes de executar.

## Uso como skill do Claude Code

### Instalação da skill

**Mac/Linux/PowerShell:**
```bash
mkdir -p .claude/commands
cp SKILL.md .claude/commands/busca-linkedin.md
```

**Windows (Prompt de Comando):**
```cmd
mkdir .claude\commands
copy SKILL.md .claude\commands\busca-linkedin.md
```

### Uso

Abra o Claude Code dentro da pasta do projeto:

```bash
claude .
```

Acione com `/busca-linkedin`. O Claude irá guiar você pela configuração das colunas, coletar as informações da planilha e executar a busca.

> **Importante:** a skill edita `config/config.json` e executa os scripts relativos à pasta do projeto. O Claude Code precisa estar aberto nessa pasta para funcionar corretamente.

## Execução manual (sem Claude Code)

Os scripts podem ser executados diretamente. Configure as colunas em `config/config.json` e leia os dados:

**Mac/Linux:**
```bash
python3 scripts/ler_planilha.py "URL_DA_PLANILHA" LINHA_INICIAL NUM_LINHAS
```

**Windows:**
```cmd
python scripts\ler_planilha.py "URL_DA_PLANILHA" LINHA_INICIAL NUM_LINHAS
```

Após salvar os resultados em `output/resultados.json`, atualize a planilha:

**Mac/Linux:**
```bash
python3 scripts/atualizar_planilha.py "URL_DA_PLANILHA" output/resultados.json
```

**Windows:**
```cmd
python scripts\atualizar_planilha.py "URL_DA_PLANILHA" output\resultados.json
```

> Não sabe qual usar? Rode `python --version` e `python3 --version` no terminal — use o que responder sem erro.

## Segurança

- As credenciais OAuth ficam apenas localmente (`%APPDATA%\gspread\` ou `~/.config/gspread/`)
- O diretório `output/` é gitignored — pode conter dados pessoais de terceiros
- `CLAUDE.md` é gitignored — cada usuário mantém sua própria configuração local
