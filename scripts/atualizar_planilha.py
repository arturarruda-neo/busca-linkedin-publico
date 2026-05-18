import json
import time
import argparse
from pathlib import Path
import gspread

CONFIG_FILE = Path(__file__).parent.parent / "config" / "config.json"


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f).get("columns", {})
    return {}


def atualizar_planilha(url, arquivo_resultados, col_contato, col_linkedin):
    gc = gspread.oauth()
    ws = gc.open_by_url(url).get_worksheet(0)

    with open(arquivo_resultados, "r", encoding="utf-8") as f:
        resultados = json.load(f)

    atualizacoes = []
    for r in resultados:
        linha = r["linha"]
        contatos = r.get("contatos", [])
        urls_linkedin = r.get("urls_linkedin", [])
        linkedin_existente = r.get("linkedin_existente", "")

        contato_str = "\n".join(contatos) if contatos else "N.A."
        url_str = "\n".join(urls_linkedin) if urls_linkedin else "N.A."

        atualizacoes.append({"range": f"{col_contato}{linha}", "values": [[contato_str]]})

        if not linkedin_existente.strip():
            atualizacoes.append({"range": f"{col_linkedin}{linha}", "values": [[url_str]]})

    if atualizacoes:
        ws.batch_update(atualizacoes)
        time.sleep(1)

    encontrados = sum(1 for r in resultados if r.get("urls_linkedin"))
    nao_encontrados = sum(1 for r in resultados if not r.get("urls_linkedin"))

    print(f"\nProcessamento concluido!")
    print(f"Total de linhas:            {len(resultados)}")
    print(f"[OK] LinkedIn encontrado:   {encontrados}")
    print(f"[--] Nao encontrado (N/A):  {nao_encontrados}")
    print(f"\nPlanilha atualizada com sucesso.")


if __name__ == "__main__":
    cfg = load_config()

    parser = argparse.ArgumentParser(description="Atualiza planilha Google Sheets com resultados de busca LinkedIn.")
    parser.add_argument("url", help="URL da planilha Google Sheets")
    parser.add_argument("arquivo_resultados", help="Caminho para o arquivo resultados.json")
    parser.add_argument("--col-contato", default=cfg.get("contato", "L"), metavar="COL", help="Coluna para gravar o contato")
    parser.add_argument("--col-linkedin", default=cfg.get("linkedin", "O"), metavar="COL", help="Coluna para gravar a URL do LinkedIn")
    args = parser.parse_args()

    atualizar_planilha(args.url, args.arquivo_resultados, args.col_contato, args.col_linkedin)
