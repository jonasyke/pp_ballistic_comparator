from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

# --- Fetch page ---
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
}
url = 'https://chuckhawks.com/rifle_ballistics_table2.htm'
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"Error fetching page: {e}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# --- Find the data table ---
tables = soup.find_all('table')
data_table = None
for i, table in enumerate(tables):
    text_snippet = table.get_text()[:200].lower()
    if 'v/e' in text_snippet or 'muzzle' in text_snippet:
        data_table = table
        print(f"Selected table {i+1} as data table.")
        break

if not data_table:
    print("No data table found.")
    exit()

# --- Extract rows ---
rows = []
for tr in data_table.find_all('tr'):
    cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
    if not cells:
        continue

    first_cell = cells[0]
    # Only keep rows where first cell looks like a caliber and at least one V/E cell exists
    if any(char.isalpha() for char in first_cell) and any('/' in c for c in cells[1:]):
        rows.append(cells[:5])  # Caliber + 4 V/E columns

# --- Build DataFrame with clean headers ---
columns = [
    "Caliber",
    "Muzzle Velocity", "Muzzle Energy",
    "100yd Velocity", "100yd Energy",
    "200yd Velocity", "200yd Energy",
    "300yd Velocity", "300yd Energy"
]

clean_rows = []
for row in rows:
    caliber_full = row[0]

    # Extract bullet type inside parentheses
    match = re.search(r'\((.*?)\)', caliber_full)
    bullet_type = match.group(1) if match else None

    # Remove parentheses from caliber name
    caliber = re.sub(r'\s*\(.*?\)', '', caliber_full).strip()

    ve_values = []
    for ve in row[1:]:
        try:
            v, e = ve.split('/')
            ve_values.extend([float(v), float(e)])
        except:
            ve_values.extend([None, None])

    clean_rows.append([caliber, bullet_type] + ve_values)

# New headers including Bullet Type
columns = [
    "Caliber", "Bullet Type",
    "Muzzle Velocity", "Muzzle Energy",
    "100yd Velocity", "100yd Energy",
    "200yd Velocity", "200yd Energy",
    "300yd Velocity", "300yd Energy"
]

df = pd.DataFrame(clean_rows, columns=columns)

# --- Save CSV ---
df.to_csv('rifle_caliber_data_clean.csv', index=False)

# --- Quick snapshot function ---
def snapshot(df, n=5):
    print("=== Columns ===")
    print(df.columns.tolist())
    print("\n=== First rows ===")
    print(df.head(n).to_string())
    print("\n=== Data types ===")
    print(df.dtypes)

snapshot(df, n=10)


