import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "google.json"

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
client = gspread.authorize(credentials)

# Intenta abrir el archivo y leer una hoja
try:
    spreadsheet = client.open("centromedico")
    worksheet = spreadsheet.empresas  # Accede a la primera hoja
    print("Acceso exitoso:", worksheet.title)
except Exception as e:
    print("Error:", e)
