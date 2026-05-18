import json
import argparse
import gspread


def col_to_idx(col_letter, start_col):
    return ord(col_letter.upper()) - ord(start_col.upper())


def ler_planilha(url, linha_inicial, num_linhas, col_empresa, col_socios, col_contato, col_linkedin):
    gc = gspread.oauth()
    ws = gc.open_by_url(url).get_worksheet(0)

    cols = [col_empresa, col_socios, col_contato, col_linkedin]
    col_inicio = min(cols, key=lambda c: ord(c.upper()))
    col_fim = max(cols, key=lambda c: ord(c.upper()))
    num_cols = ord(col_fim.upper()) - ord(col_inicio.upper()) + 1

    linha_final = linha_inicial + num_linhas - 1
    rows = ws.get(f"{col_inicio}{linha_inicial}:{col_fim}{linha_final}", value_render_option="UNFORMATTED_VALUE")

    resultado = []
    for i, row in enumerate(rows):
        while len(row) < num_cols:
            row.append("")

        def get_col(letra):
            return str(row[col_to_idx(letra, col_inicio)]).strip()

        socios = [s.strip() for s in get_col(col_socios).split("\n") if s.strip()]

        resultado.append({
            "linha": linha_inicial + i,
            "nome_empresa": get_col(col_empresa),
            "socios": socios,
            "contato": get_col(col_contato),
            "linkedin_existente": get_col(col_linkedin),
        })

    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lê dados de empresas e sócios de uma planilha Google Sheets.")
    parser.add_argument("url", help="URL da planilha Google Sheets")
    parser.add_argument("linha_inicial", type=int, help="Linha inicial dos dados")
    parser.add_argument("num_linhas", type=int, help="Número de linhas a ler")
    parser.add_argument("--col-empresa", default="C", metavar="COL", help="Coluna do nome da empresa (padrão: C)")
    parser.add_argument("--col-socios", default="K", metavar="COL", help="Coluna dos sócios separados por quebra de linha (padrão: K)")
    parser.add_argument("--col-contato", default="L", metavar="COL", help="Coluna para gravar o contato encontrado (padrão: L)")
    parser.add_argument("--col-linkedin", default="O", metavar="COL", help="Coluna para gravar a URL do LinkedIn (padrão: O)")
    args = parser.parse_args()

    ler_planilha(
        args.url, args.linha_inicial, args.num_linhas,
        args.col_empresa, args.col_socios, args.col_contato, args.col_linkedin,
    )
