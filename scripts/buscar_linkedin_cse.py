import os
import sys
from pathlib import Path

import gspread
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

API_KEY = os.environ["GOOGLE_CSE_API_KEY"]
CSE_ID = os.environ["GOOGLE_CSE_ID"]
CSE_URL = "https://www.googleapis.com/customsearch/v1"
MAX_WORKERS = 5


def buscar_linkedin_socio(socio, empresa):
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": f"{socio} {empresa} site:linkedin.com/in",
        "num": 3,
    }
    try:
        resp = requests.get(CSE_URL, params=params, timeout=10)
        resp.raise_for_status()
        for item in resp.json().get("items", []):
            if "linkedin.com/in/" in item.get("link", ""):
                return item["link"]
    except Exception:
        pass
    return None


def processar_empresa(dados):
    linha = dados["linha"]
    nome_empresa = dados["nome_empresa"]
    socios = dados["socios"]
    contato_existente = dados["contato"]
    linkedin_existente = dados["linkedin_existente"]

    if contato_existente and contato_existente != "N.A.":
        return {
            "linha": linha,
            "nome_empresa": nome_empresa,
            "contato": contato_existente,
            "url_linkedin": "",
            "linkedin_existente": linkedin_existente,
            "status": "pulado",
        }

    for socio in socios:
        url = buscar_linkedin_socio(socio, nome_empresa)
        if url:
            return {
                "linha": linha,
                "nome_empresa": nome_empresa,
                "contato": socio,
                "url_linkedin": url,
                "linkedin_existente": linkedin_existente,
                "status": "encontrado",
            }

    return {
        "linha": linha,
        "nome_empresa": nome_empresa,
        "contato": "N.A.",
        "url_linkedin": "",
        "linkedin_existente": linkedin_existente,
        "status": "nao_encontrado",
    }


def ler_planilha(ws, linha_inicial, num_linhas):
    linha_final = linha_inicial + num_linhas - 1
    rows = ws.get(f"B{linha_inicial}:P{linha_final}", value_render_option="UNFORMATTED_VALUE")

    resultado = []
    for i, row in enumerate(rows):
        while len(row) < 15:
            row.append("")

        socios_raw = str(row[9]) if row[9] else ""
        socios = [s.strip() for s in socios_raw.split("\n") if s.strip()]

        resultado.append({
            "linha": linha_inicial + i,
            "nome_empresa": str(row[1]).strip(),
            "socios": socios,
            "contato": str(row[10]).strip(),
            "linkedin_existente": str(row[13]).strip(),
        })

    return resultado


def atualizar_planilha(ws, resultados):
    atualizacoes = []
    for r in resultados:
        if r["status"] == "pulado":
            continue

        atualizacoes.append({"range": f"L{r['linha']}", "values": [[r["contato"]]]})

        if r["url_linkedin"] and not r["linkedin_existente"].strip():
            atualizacoes.append({"range": f"O{r['linha']}", "values": [[r["url_linkedin"]]]})

    if atualizacoes:
        ws.batch_update(atualizacoes)


def main():
    if len(sys.argv) < 4:
        print("Uso: python buscar_linkedin_cse.py <URL> <linha_inicial> <num_linhas>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    linha_inicial = int(sys.argv[2])
    num_linhas = int(sys.argv[3])

    gc = gspread.oauth()
    ws = gc.open_by_url(url).get_worksheet(0)

    print(f"Lendo linhas {linha_inicial} a {linha_inicial + num_linhas - 1}...")
    dados = ler_planilha(ws, linha_inicial, num_linhas)

    a_processar = [d for d in dados if not d["contato"] or d["contato"] == "N.A."]
    pulados = len(dados) - len(a_processar)

    print(f"Empresas a processar: {len(a_processar)} | Ja preenchidas (puladas): {pulados}")
    print(f"Buscando no LinkedIn ({MAX_WORKERS} em paralelo)...\n")

    resultados_novos = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(processar_empresa, d): d for d in a_processar}
        for future in as_completed(futures):
            r = future.result()
            resultados_novos.append(r)
            icone = "[OK]" if r["status"] == "encontrado" else "[--]"
            print(f"  {icone} {r['nome_empresa']}: {r['contato']}")

    resultados_novos.sort(key=lambda x: x["linha"])

    print("\nAtualizando planilha...")
    atualizar_planilha(ws, resultados_novos)

    encontrados = sum(1 for r in resultados_novos if r["status"] == "encontrado")
    nao_encontrados = sum(1 for r in resultados_novos if r["status"] == "nao_encontrado")

    print(f"\nProcessamento concluido!")
    print(f"Total de linhas:            {len(dados)}")
    print(f"[OK] LinkedIn encontrado:   {encontrados}")
    print(f"[--] Nao encontrado (N/A):  {nao_encontrados}")
    if pulados:
        print(f"[>>] Pulados (ja tinham):   {pulados}")
    print("\nPlanilha atualizada com sucesso.")


if __name__ == "__main__":
    main()
