import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_ballistics_table(url):
    """
    Scrapes the rifle ballistics table from the given URL and returns it as a pandas DataFrame.
    Splits V/E columns into separate velocity and energy columns.
    
    Args:
        url (str): The URL of the webpage containing the table.
    
    Returns:
        pd.DataFrame: A DataFrame with the table data, split into velocity and energy columns.
    """
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Fetch the webpage content
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch the webpage: {e}")
    
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all tables
    tables = soup.find_all('table')
    if not tables:
        raise ValueError("No tables found on the page.")
    
    # Debug: Print headers of each table to inspect
    print(f"Found {len(tables)} table(s). Inspecting headers...")
    target_table = None
    for i, table in enumerate(tables):
        # Try to find headers in <th> or <td> (first row)
        rows = table.find_all('tr')
        if not rows:
            continue
        first_row = rows[0]
        headers = [cell.text.strip() for cell in first_row.find_all(['th', 'td'])]
        print(f"Table {i + 1} headers: {headers}")
        # Check if the expected header is present (partial match for robustness)
        if any('Cartridge' in header for header in headers):
            target_table = table
            break
    
    if not target_table:
        raise ValueError("No table found with headers containing 'Cartridge'.")
    
    # Extract headers and rows
    headers = [cell.text.strip() for cell in target_table.find('tr').find_all(['th', 'td'])]
    rows = target_table.find_all('tr')[1:]  # Skip header row
    
    # Extract data
    data = []
    for row in rows:
        cols = row.find_all('td')
        row_data = [col.text.strip() if col.text.strip() else None for col in cols]
        if row_data and len(row_data) == len(headers):  # Ensure row has correct number of columns
            data.append(row_data)
    
    if not data:
        raise ValueError("No data extracted from the table.")
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)
    
    # Function to split V/E columns (e.g., '3650/592' -> velocity: 3650, energy: 592)
    def split_ve(ve_str):
        if ve_str and '/' in ve_str:
            try:
                v, e = ve_str.split('/')
                return pd.Series([int(v.strip()), int(e.strip())])
            except (ValueError, AttributeError):
                return pd.Series([None, None])
        return pd.Series([None, None])
    
    # Split V/E columns into separate velocity and energy columns
    for col in headers[1:]:  # Skip the 'Cartridge (Wb + type)' column
        df[[f'Velocity {col[4:]}', f'Energy {col[4:]}']] = df[col].apply(split_ve)
       