# Design — Organização do Projeto busca-linkedin

**Data:** 2026-04-29
**Escopo:** Limpeza cirúrgica (estrutura + código). Sem novos scripts. Sem mudança de comportamento.

## Mudanças

### 1. `.gitignore` (novo arquivo)
Excluir `output/resultados.json` do controle de versão. Arquivo gerado a cada execução.

### 2. `requirements.txt` (novo arquivo)
```
gspread>=6.0.0
google-auth-oauthlib>=1.0.0
```

### 3. Criar pasta `output/`
Destino do `resultados.json` gerado durante execução. Separa artefatos de execução do código-fonte.

### 4. `.claude/settings.local.json` — remover permissões obsoletas
Quatro entradas de comandos de setup one-time já executados (mkdir, mv, dois cp). Manter apenas `Bash(python *)` e `WebSearch`.

### 5. `scripts/atualizar_planilha.py` — remover comentários de QUÊ
- Remover: `# Coluna K (índice 11) = Contato — sempre atualiza`
- Remover: `# Envia todas as atualizações de uma vez (batch) para eficiência`
- Manter: `# respeitar rate limit da API`

### 6. SKILL.md global — corrigir caminhos de scripts e path do resultados.json
Arquivo: `C:\Users\MF Capital\.claude\plugins\busca-linkedin\skills\busca-linkedin\SKILL.md`

- Passo 3: substituir caminho do `ler_planilha.py` (plugin → projeto)
- Passo 5: substituir `resultados.json` por `output/resultados.json`
- Passo 5: substituir caminho do `atualizar_planilha.py` (plugin → projeto)

Caminhos corretos:
```
C:/secret-sauce/busca-linkedin/scripts/ler_planilha.py
C:/secret-sauce/busca-linkedin/scripts/atualizar_planilha.py
C:/secret-sauce/busca-linkedin/output/resultados.json
```

### 7. Remover `SKILL.md` do projeto
Cópia redundante — versão canônica está no diretório global de plugins.

### 8. Atualizar `CLAUDE.md` do projeto
- Remover `SKILL.md` da seção "Estrutura do Repositório"
- Adicionar `output/` à estrutura
- Corrigir seção "Arquivos da Skill" — os scripts canônicos são os do projeto, não os do plugin

## Fora do escopo
- Extração de utilitários compartilhados entre scripts
- Integração com busca de e-mails (será skill separada com Apollo API)
