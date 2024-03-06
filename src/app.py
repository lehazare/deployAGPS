from dash import Dash, html, dcc, Input, Output
from data.data_loader import load_market, load_portfolio
from callbacks.output_generator import output_generator_callback
from callbacks.date_picker import update_date_picker_callback
from callbacks.update_graph import update_market_graphs_callback, update_portfolio_graph_callback
from callbacks.update_table import update_market_tables_callback, update_portfolio_table_callback, update_rebalancing_table_callback
from pages import overview, pricePerformance, portfolioManagement

# Initialize the Dash app with external CSS
app = Dash(__name__, suppress_callback_exceptions=True)

server = app.server

# Load data
close_price_df, close_ret_df, taux_interet_df, xfor_price_df, xfor_ret_df = load_market()
portfolio_df = load_portfolio()

# Describe the layout/ UI of the app
app.layout = html.Div([
    dcc.Store(id='memory'),
    dcc.Location(id="url", refresh=False), html.Div(id="page-content")
    ])

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/price-performance":
        return pricePerformance.create_layout(app)
    elif pathname == "/portfolio-management":
        return portfolioManagement.create_layout(app)
    else:
        return overview.create_layout(app)

# Register the date picker callback
update_date_picker_callback(app, close_price_df)

# Callback to update the graphs
update_market_graphs_callback(app, close_price_df)

# Callback to update the tables
update_market_tables_callback(app, close_price_df)

# Callback to update the portfolio table
update_portfolio_table_callback(app, portfolio_df, close_price_df, taux_interet_df, xfor_price_df)

# Callback to update the rebalancing table
update_rebalancing_table_callback(app, portfolio_df, close_price_df)

# Register the callback
output_generator_callback(app, close_price_df, close_ret_df, taux_interet_df, xfor_price_df, xfor_ret_df)

# Update the portfolio graph
update_portfolio_graph_callback(app, portfolio_df, close_price_df)

if __name__ == '__main__':
    app.run(debug=True)
