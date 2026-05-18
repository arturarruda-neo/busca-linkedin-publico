from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDENTIALS_FILE = Path(r"C:\Users\MF Capital\AppData\Roaming\gspread\credentials.json")
TOKEN_FILE = Path(r"C:\Users\MF Capital\AppData\Roaming\gspread\authorized_user.json")

flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
print("\nAbrindo servidor local na porta 8080...")
print("Uma URL será exibida abaixo — abra-a no navegador:\n")
creds = flow.run_local_server(port=8080, open_browser=False)

TOKEN_FILE.write_text(creds.to_json())
print(f"\nToken salvo em: {TOKEN_FILE}")
