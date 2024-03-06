from dash import Input, Output, State
from data.kanji90 import set1, set2, set3
from builders.plot_builder import plot_market, plot_portfolio
import plotly.graph_objs as go

def update_market_graphs_callback(app, df):
    # Register the callback to update the graph
    @app.callback(
        [Output('graph1', 'figure'),
         Output('graph2', 'figure'),
         Output('graph3', 'figure')],
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
        
        plot1 = go.Figure()
        plot2 = go.Figure()
        plot3 = go.Figure()

        if current_date is not None:
            plot1, plot2, plot3 = plot_market(df, selected_set, current_date)

        return plot1, plot2, plot3

def update_portfolio_graph_callback(app, df_portfolio, df_market):
    # Register the callback to update the graph
    @app.callback(
        Output('portfolio-graph', 'figure'),
        Input('rebalance-button', 'n_clicks'),
        Input('date-set-dropdown', 'value'),
        State('memory', 'data'),
    )
    def update_portfolio_graph(n_clicks, selected_set, data):
        if selected_set == 'set1':
            selected_set = set1
        elif selected_set == 'set2':
            selected_set = set2
        elif selected_set == 'set3':
            selected_set = set3

        return plot_portfolio(df_portfolio, df_market, selected_set, data['date'], n_clicks)
