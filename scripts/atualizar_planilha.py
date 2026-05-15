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
        linkedin_existente = r.get("linkedin_existente", "")

        atualizacoes.append({
            "range": f"L{linha}",
            "values": [[contato]],
        })

        if url_linkedin and not linkedin_existente.strip():
            atualizacoes.append({
                "range": f"O{linha}",
                "values": [[url_linkedin]],
            })

    if atualizacoes:
        ws.batch_update(atualizacoes)
        time.sleep(1)  # respeitar rate limit da API

    encontrados = sum(1 for r in resultados if r.get("url_linkedin"))
    nao_encontrados = sum(1 for r in resultados if not r.get("url_linkedin"))
    linkedin_ja_preenchido = sum(
        1 for r in resultados
        if r.get("url_linkedin") and r.get("linkedin_existente", "").strip()
    )

    print(f"\nProcessamento concluido!")
    print(f"Total de linhas:         {len(resultados)}")
    print(f"[OK] LinkedIn encontrado:   {encontrados}")
    print(f"[--] Nao encontrado (N/A):  {nao_encontrados}")
    if linkedin_ja_preenchido:
        print(f"[~~] LinkedIn ja preenchido: {linkedin_ja_preenchido} (URL nao sobrescrita)")
    print(f"\nPlanilha atualizada com sucesso.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python atualizar_planilha.py <URL> <resultados.json>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    arquivo = sys.argv[2]
    atualizar_planilha(url, arquivo)
