from datetime import datetime
import pandas as pd
from data.kanji90 import set1

def table_market(df, selected_set, current_date):

    # Sélectionner les colonnes "S&P500", "HANGSENG" & "EUROSTOXX50" pour l'ensemble sélectionné
    selected_columns = ["Date", "EUROSTOXX50", "SP500", "HANGSENG"]
    selected_data = df[selected_columns].copy()

    # Convertir la colonne "Date" en objets date Python
    selected_data["Date"] = pd.to_datetime(selected_data["Date"]).dt.date

    current_date = datetime.strptime(current_date, '%Y-%m-%d').date()

    # Calculate Daily Performance
    yesterday = (current_date - pd.DateOffset(days=1)).date()
    daily_performance = (find_the_data(selected_data, current_date) - find_the_data(selected_data, yesterday))/find_the_data(selected_data, yesterday)
    daily_performance = daily_performance.loc[0] * 100

    # Calculate 6-Months Performance
    six_months_ago = (current_date - pd.DateOffset(months=6)).date()
    six_months_performance = (find_the_data(selected_data, current_date) - find_the_data(selected_data, six_months_ago))/find_the_data(selected_data, six_months_ago)
    six_months_performance = six_months_performance.loc[0] * 100


    # Calculate Yearly Performance
    one_year_ago = (current_date - pd.DateOffset(years=1)).date()
    one_year_performance = (find_the_data(selected_data, current_date) - find_the_data(selected_data, one_year_ago))/find_the_data(selected_data, one_year_ago)
    one_year_performance = one_year_performance.loc[0] * 100
   

    # Create DataFrames for each index
    table_Eurostoxx50 = pd.DataFrame({
        "Performances": ["Daily (in %)", "6-Months (in %)", "Year (in %)"],
        "Values": [round(daily_performance["EUROSTOXX50"], 2),
                round(six_months_performance["EUROSTOXX50"], 2),
                round(one_year_performance["EUROSTOXX50"], 2)],
    }, index=["Daily Performance (in %)", "6-Months Performance (in %)", "Year Performance (in %)"])

    table_SP500 = pd.DataFrame({
        "Performances": ["Daily (in %)", "6-Months (in %)", "Year (in %)"],
        "Values": [round(daily_performance["SP500"], 2),
                round(six_months_performance["SP500"], 2),
                round(one_year_performance["SP500"], 2)],
    }, index=["Daily Performance (in %)", "6-Months Performance (in %)", "Year Performance (in %)"])

    table_HangSeng = pd.DataFrame({
        "Performances": ["Daily (in %)", "6-Months (in %)", "Year (in %)"],
        "Values": [round(daily_performance["HANGSENG"], 2),
                round(six_months_performance["HANGSENG"], 2),
                round(one_year_performance["HANGSENG"], 2)],
    }, index=["Daily Performance (in %)", "6-Months Performance (in %)", "Year Performance (in %)"])

    return table_Eurostoxx50, table_SP500, table_HangSeng

def table_portfolio(df_portfolio, df_market, df_rates, df_change, selected_set, current_date):

    #################### Parser les quantités d'actifs (deltas) ####################

    quantity = [787.8, -301, -2457, 0.0853, 0.320, 0.156]
    # quantity = [1000, 0, 0, 0, 0, 0]

    #################### Parser les prix foreigners ####################

    # Sélectionner les derniers prix pour les taux
    selected_columns = ["RAUD", "REUR", "RUSD", "RHKD"]
    selected_rates = df_rates[selected_columns].copy()
    selected_rates.rename(columns={"RAUD": "Date"}, inplace=True)
    selected_rates["Date"] = pd.to_datetime(selected_rates["Date"]).dt.date
    current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
    selected_rates = find_the_data(selected_rates, current_date)
    selected_rates = selected_rates.iloc[0]

    # Sélectionner les derniers prix pour les indices
    selected_columns = ["Date", "EUROSTOXX50", "SP500", "HANGSENG"]
    selected_benchmark = df_market[selected_columns].copy()
    selected_benchmark["Date"] = pd.to_datetime(selected_benchmark["Date"]).dt.date
    selected_benchmark = find_the_data(selected_benchmark, current_date)
    selected_benchmark = selected_benchmark.iloc[0]

    foreigner_prices = [selected_rates["REUR"], selected_rates["RUSD"], selected_rates["RHKD"], selected_benchmark["EUROSTOXX50"], selected_benchmark["SP500"], selected_benchmark["HANGSENG"]]

    #################### Parser les prix euros ####################

    selected_columns = ["Date", "XUSD", "XHKD"]
    selected_change = df_change[selected_columns].copy()
    selected_change["Date"] = pd.to_datetime(selected_change["Date"]).dt.date
    selected_change = find_the_data(selected_change, current_date)
    selected_change = selected_change.iloc[0]

    list_of_change = [1, selected_change["XUSD"], selected_change["XHKD"], 1, selected_change["XUSD"], selected_change["XHKD"]]
    euros_prices = [a*b for a, b in zip(foreigner_prices, list_of_change)]

    #################### Calculer les quantitées totales investies ####################

    list_for_total = [1, 1, 1, euros_prices[3], euros_prices[4], euros_prices[5]]
    total_quantity_invested = [a*b for a, b in zip(quantity, list_for_total)]

    table = pd.DataFrame({
        "Product Name": ["REUR", "RUSD", "RHKG", "EUROSTOXX50", "SP500", "HANGSENG"],
        "Quantity": list(map(lambda x: round(x, 4), quantity)),
        "Price (in €)" : list(map(lambda x: round(x, 4), euros_prices)),
        "Price (in foreign currency)": list(map(lambda x: round(x, 4), foreigner_prices)),
        "Total quantity investested": list(map(lambda x: round(x, 4), total_quantity_invested)),
    })

    return table

def table_rebalancing(df_portfolio, df_market, selected_set):
    table = pd.DataFrame({
        "Product Name": ["REUR", "RUSD", "RHKG", "EUROSTOXX50", "SP500", "HANGSENG"],
        "Previous Quantity" : [1000.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "New Quantity" : [799.67, 76.92, 0.0, 0.0, 0.0, 0.0],
    })

    return table

def find_the_data(df, date):
    if date <= datetime.strptime("05/01/2000", "%d/%m/%Y").date():
        date = datetime.strptime("05/01/2000", "%d/%m/%Y").date()
        return df[df["Date"] == date].reset_index(drop=True).iloc[:, 1:]

    if date in df["Date"].values and not df[df["Date"] == date].reset_index(drop=True).iloc[:, 1:].isna().any().any():
        return df[df["Date"] == date].reset_index(drop=True).iloc[:, 1:]
    else:
        while date not in df["Date"].values or df[df["Date"] == date].reset_index(drop=True).iloc[:, 1:].isna().any().any():
            date = (date - pd.DateOffset(days=1)).date()
        return df[df["Date"] == date].reset_index(drop=True).iloc[:, 1:]