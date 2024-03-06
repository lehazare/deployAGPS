from dash import Input, Output, html, dash_table
from data.kanji90 import set1, set2, set3
from builders.table_builder import table_market, table_portfolio, table_rebalancing
import pandas as pd

def update_market_tables_callback(app, df):
    # Register the callback to update the graph
    @app.callback(
        [Output('table1', 'data'),
         Output('table2', 'data'),
         Output('table3', 'data')],
        [Input('date-set-dropdown', 'value'),
         Input('my-date-picker-single', 'date')]
    )
    def update_graph(selected_set, current_date):
        if selected_set == 'set1':
            selected_set = set1
        elif selected_set == 'set2':
            selected_set = set2
        else:
            selected_set = set3

        table_Eurostoxx50 = pd.DataFrame({
            "Performances": ["Daily (in %)", "6-Months (in %)", "Year (in %)"],
            "Values": [0, 0, 0],
        }, index=["Daily Performance (in %)", "6-Months Performance (in %)", "Year Performance (in %)"])

        table_SP500 = pd.DataFrame({
            "Performances": ["Daily (in %)", "6-Months (in %)", "Year (in %)"],
            "Values": [0, 0, 0],
        }, index=["Daily Performance (in %)", "6-Months Performance (in %)", "Year Performance (in %)"])

        table_HangSeng = pd.DataFrame({
            "Performances": ["Daily (in %)", "6-Months (in %)", "Year (in %)"],
            "Values": [0, 0, 0],
        }, index=["Daily Performance (in %)", "6-Months Performance (in %)", "Year Performance (in %)"])

        if current_date is not None:
            table_Eurostoxx50, table_SP500, table_HangSeng = table_market(df, selected_set, current_date)  

        return table_Eurostoxx50.to_dict('records'), table_SP500.to_dict('records'), table_HangSeng.to_dict('records')
    

def update_portfolio_table_callback(app, df_portfolio, df_market, df_rates, df_change):
    # Register the callback to update the graph
    @app.callback(
        Output('portfolio-information-table', 'data'),
        Input('rebalance-button', 'n_clicks'),
        Input('date-set-dropdown', 'value'),
        Input('my-date-picker-single', 'date')
    )
    def update_portfolio_graph(n_clicks, selected_set, current_date):

        table = pd.DataFrame({
            "Product Name": ["REUR", "RUSD", "RHKG", "EUROSTOXX50", "SP500", "HANGSENG"],
            "Quantity": [0, 0, 0, 0, 0, 0],
            "Price (in €)" : [0, 0, 0, 0, 0, 0],
            "Price (in foreign currency)": [0, 0, 0, 0, 0, 0],
            "Total quantity investested": [0, 0, 0, 0, 0, 0],
        })

        if current_date is not None:
            table = table_portfolio(df_portfolio, df_market, df_rates, df_change, selected_set, current_date)

        return table.to_dict('records')
    
def update_rebalancing_table_callback(app, df_portfolio, df_market):
    # Register the callback to update the graph
    @app.callback(
        Output('rebalancing-information-table', 'data'),
        Input('rebalance-button', 'n_clicks'),
        Input('date-set-dropdown', 'value'),
    )
    def update_portfolio_graph(n_clicks, selected_set):
   
        table = table_rebalancing(df_portfolio, df_market, selected_set)

        return table.to_dict('records')