from datetime import datetime
import json
from dash import Output, Input, html, State
import os
import pandas as pd
import numpy as np
from data.kanji90 import set1, set2, set3

def output_generator_callback(app, close_price_df, close_ret_df, taux_interet_df, xfor_price_df, xfor_ret_df):
    @app.callback(
        Output('output-answer', 'children'),
        Input('generate-csv-button', 'n_clicks'),
        State('my-date-picker-single', 'date'),
        State('date-set-dropdown', 'value')
    )
    def csv_json(n_clicks, current_date, selected_set):

##################################### EXTRACTING DATA #####################################

        if n_clicks is not None:
            if selected_set == 'set1':
                selected_set = set1
            elif selected_set == 'set2':
                selected_set = set2
            else:
                selected_set = set3

            # Sélectionner les colonnes "S&P500", "HANGSENG" & "EUROSTOXX50" for the selected set
            selected_columns = ["Date", "EUROSTOXX50", "SP500", "HANGSENG"]
            full_data = close_price_df[selected_columns].copy()

            ########## Dates Management ##########

            # Convert the "Date" column to Python date objects
            full_data["Date"] = pd.to_datetime(full_data["Date"]).dt.date

            # Ensure that selected_set['T0'] and selected_set['Tc'] are Python date objects
            selected_set['T0'] = datetime.strptime(selected_set['T0'].strftime("%m/%d/%Y"), "%m/%d/%Y").date()
            current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
            
            # Filter data based on selected set's T0 and Now
            data_from_T0_until_Now = full_data[(full_data["Date"] >= selected_set['T0']) & (full_data["Date"] <= current_date)]

            # Filter data based on selected set's beginning and Now
            data_from_Beginning_until_Now = full_data[(full_data["Date"] <= current_date)]

            ########## interest rates ##########
            selected_columns = ["RAUD", "REUR", "RUSD", "RHKD"]
            selected_rates = taux_interet_df[selected_columns].copy()
            selected_rates.rename(columns={"RAUD": "Date"}, inplace=True)
            selected_rates["Date"] = pd.to_datetime(selected_rates["Date"]).dt.date
            data_from_Beginning_until_Now = data_from_Beginning_until_Now.merge(selected_rates, on="Date")

            ################ XFOR ################
            selected_columns = ["Date", "XUSD", "XHKD"]
            selected_xfor = xfor_price_df[selected_columns].copy()
            selected_xfor["Date"] = pd.to_datetime(selected_xfor["Date"]).dt.date
            data_from_T0_until_Now = data_from_T0_until_Now.merge(selected_xfor, on="Date")
            data_from_Beginning_until_Now = data_from_Beginning_until_Now.merge(selected_xfor, on="Date")

            ############### Returns ##############

            # Add the close returns to the DataFrame
            selected_columns = ["Date", "EUROSTOXX50", "SP500", "HANGSENG"]
            selected_close_ret = close_ret_df[selected_columns].copy()
            selected_close_ret["Date"] = pd.to_datetime(selected_close_ret["Date"]).dt.date
            selected_close_ret.rename(columns={"EUROSTOXX50": "EUROSTOXX50r", "SP500": "SP500r", "HANGSENG": "HANGSENGr"}, inplace=True)
            data_from_Beginning_until_Now = data_from_Beginning_until_Now.merge(selected_close_ret, on="Date")

            # Add the XFOR returns to the DataFrame
            selected_columns = ["Date", "XUSD", "XHKD"]
            selected_xfor_ret = xfor_ret_df[selected_columns].copy()
            selected_xfor_ret["Date"] = pd.to_datetime(selected_xfor_ret["Date"]).dt.date
            selected_xfor_ret.rename(columns={"XUSD": "XUSDr", "XHKD": "XHKDr"}, inplace=True)
            data_from_Beginning_until_Now = data_from_Beginning_until_Now.merge(selected_xfor_ret, on="Date")

############################################ CSV ############################################

            # Create directory if it doesn't exist
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save DataFrame to CSV
            output_csv = os.path.join(output_dir, 'market.csv')
            #data_from_T0_until_Now.to_csv(output_csv, index=True, header=True)
            data_from_T0_until_Now.drop(columns = ["Date"]).to_csv(output_csv, index=False, header=False)

############################################ JSON ############################################
            
            data = {
                "CurrentDate": int(full_data[full_data["Date"] == current_date].index.values[0])-int(full_data[full_data["Date"] == selected_set['T0']].index.values[0]),
                "DomesticCurrencyId": "eur",
                "DomesticInterestRate": data_from_Beginning_until_Now["REUR"].iloc[-1],
                "Assets": [
                    {
                    "CurrencyId": "eur",
                    "Volatility": data_from_Beginning_until_Now["EUROSTOXX50r"].apply(lambda x: np.log1p(x)).std()
                    },
                    {
                    "CurrencyId": "us_dollar",
                    "Volatility": data_from_Beginning_until_Now["SP500"].apply(lambda x: np.log1p(x)).std()
                    },
                    {
                    "CurrencyId": "hk_dollar",
                    "Volatility": data_from_Beginning_until_Now["HANGSENG"].apply(lambda x: np.log1p(x)).std()
                    },
                ],
                "Currencies": [
                    {
                    "CurrencyId": "us_dollar",
                    "Volatility": data_from_Beginning_until_Now["XUSD"].apply(lambda x: np.log1p(x)).std(),
                    "ForeignInterestRate": data_from_Beginning_until_Now["RUSD"].iloc[-1]
                    },
                    {
                    "CurrencyId": "hk_dollar",
                    "Volatility": data_from_Beginning_until_Now["XHKD"].apply(lambda x: np.log1p(x)).std(),
                    "ForeignInterestRate" : data_from_Beginning_until_Now["RHKD"].iloc[-1]
                    }
                ],
                "NumberOfDaysInYears": 252,
                "FixingDatesInDays": {
                    "DatesInDays": [ 0, 
                                    int(full_data[full_data["Date"] == selected_set['T1']].index.values[0])-int(full_data[full_data["Date"] == selected_set['T0']].index.values[0]),
                                    int(full_data[full_data["Date"] == selected_set['T2']].index.values[0])-int(full_data[full_data["Date"] == selected_set['T0']].index.values[0]),
                                    int(full_data[full_data["Date"] == selected_set['T3']].index.values[0])-int(full_data[full_data["Date"] == selected_set['T0']].index.values[0]),
                                    int(full_data[full_data["Date"] == selected_set['T4']].index.values[0])-int(full_data[full_data["Date"] == selected_set['T0']].index.values[0]),
                                    int(full_data[full_data["Date"] == selected_set['Tc']].index.values[0])-int(full_data[full_data["Date"] == selected_set['T0']].index.values[0])
                                    ],
                    "MaturityInDays": int(full_data[full_data["Date"] == selected_set['Tc']].index.values[0])-int(full_data[full_data["Date"] == selected_set['T0']].index.values[0]),
                },
                "Correlations": data_from_Beginning_until_Now[["EUROSTOXX50", "SP500", "HANGSENG", "XUSD", "XHKD"]].corr().values.tolist(),
                "SampleNb": 50000,
                "RelativeFiniteDifferenceStep": 0.1
                }
        
            # Create directory if it doesn't exist
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Serialize the data to JSON format
            json_data = json.dumps(data, indent=4)

            # Save JSON to file
            output_json = os.path.join(output_dir, 'params.json')
            with open(output_json, 'w') as file:
                file.write(json_data)

            return html.Div("CSV & JSON file generated")