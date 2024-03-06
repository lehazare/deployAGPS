import pandas as pd
import os

def load_market():
    # Charger le fichier Excel
    xlsx_file = "DonneesGPS2024.xlsx"
    chemin = os.path.join(os.path.dirname(__file__), xlsx_file)

    # Charger la page ClosePrice du fichier Excel
    close_price_df = pd.read_excel(chemin, sheet_name="ClosePrice")

    # Charger la page CloseRet du fichier Excel
    close_ret_df = pd.read_excel(chemin, sheet_name="CloseRet")

    # Charger la page TauxInteret du fichier Excel
    taux_interet_df = pd.read_excel(chemin, sheet_name="TauxInteret")

    # Charger la page XFORPrice du fichier Excel
    xfor_price_df = pd.read_excel(chemin, sheet_name="XFORPrice")

    # Charger la page XFORRet du fichier Excel
    xfor_ret_df = pd.read_excel(chemin, sheet_name="XFORRet")

    return close_price_df, close_ret_df, taux_interet_df, xfor_price_df, xfor_ret_df


def load_portfolio():

    # Charger le fichier JSON
    FILE = "./data/portfolio.json"

    df = pd.read_json(FILE, convert_dates=['date'])
    df.sort_values(by='date', inplace=True)
    df.set_index('date', inplace=True)

    return df