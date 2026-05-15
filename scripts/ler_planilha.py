import sys
import json
import gspread


def ler_planilha(url, linha_inicial, num_linhas):
    gc = gspread.oauth()
    sh = gc.open_by_url(url)
    ws = sh.get_worksheet(0)

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

    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python ler_planilha.py <URL> <linha_inicial> <num_linhas>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    linha_inicial = int(sys.argv[2])
    num_linhas = int(sys.argv[3])
    ler_planilha(url, linha_inicial, num_linhas)
