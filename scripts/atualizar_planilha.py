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
        contatos = r.get("contatos", [])
        urls_linkedin = r.get("urls_linkedin", [])
        linkedin_existente = r.get("linkedin_existente", "")

        contato_str = "\n".join(contatos) if contatos else "N.A."
        url_str = "\n".join(urls_linkedin) if urls_linkedin else "N.A."

        atualizacoes.append({"range": f"L{linha}", "values": [[contato_str]]})

        if not linkedin_existente.strip():
            atualizacoes.append({"range": f"O{linha}", "values": [[url_str]]})

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
    if len(sys.argv) < 3:
        print("Uso: python atualizar_planilha.py <URL> <resultados.json>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    arquivo = sys.argv[2]
    atualizar_planilha(url, arquivo)
