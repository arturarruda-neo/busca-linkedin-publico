import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

if os.name == "nt":
    config_dir = Path(os.environ["APPDATA"]) / "gspread"
else:
    config_dir = Path.home() / ".config" / "gspread"

credentials_file = config_dir / "credentials.json"
token_file = config_dir / "authorized_user.json"

if not credentials_file.exists():
    print(f"Erro: credenciais não encontradas em {credentials_file}")
    print("Baixe o credentials.json do Google Cloud Console e salve neste caminho.")
    raise SystemExit(1)

flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), SCOPES)
print("\nServidor local iniciado na porta 8080.")
print("Abra a URL abaixo no navegador para autorizar:\n")
creds = flow.run_local_server(port=8080, open_browser=False)

token_file.write_text(creds.to_json())
print(f"\nToken salvo em: {token_file}")
