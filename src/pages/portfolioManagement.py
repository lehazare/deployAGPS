from dash import dcc, html, dash_table
from pages.utils import Header, Dates

def create_layout(app):
    return html.Div([
        Header(app),
        Dates(app),
        html.Div([
            html.H4('Portfolio Information'),
            # html.Table(id='portfolio-information-table'),
            dash_table.DataTable(id='portfolio-information-table',
                                 style_cell={'background-color': '#007bff',
                                             'minWidth': '250px', 'width': '250px', 'maxWidth': '250px',
                                             'text_align': 'center'},
                                 style_header={'fontWeight': 'bold'},
                                 cell_selectable = False,
                                 style_cell_conditional=[
                                     {
                                         'if': {'column_id': c},
                                         'fontWeight': 'bold'
                                     } for c in ['Product Name']
                                 ],
                                 style_as_list_view=True,
                                ),
        ], className='portfolio-information-container'),
        html.Div([
            html.Div([
                html.H4('Rebalancing Information'),
                dash_table.DataTable(id='rebalancing-information-table',
                                    style_cell={'background-color': '#cc8cff',
                                                'minWidth': '250px', 'width': '250px', 'maxWidth': '250px',
                                                'text_align': 'center'},
                                    style_header={'fontWeight': 'bold'},
                                    cell_selectable = False,
                                    style_cell_conditional=[
                                        {
                                            'if': {'column_id': c},
                                            'fontWeight': 'bold'
                                        } for c in ['Product Name']
                                    ],
                                    style_as_list_view=True,
                                    ),
            ], className='rebalancing-information-container'),
            html.Div([
                html.Div([
                    html.H4('P&L'),
                    html.Span('-6.195%', id='pnl-value'),
                ], className='pnl-container'),
                html.Div([
                    html.H4('Value'),
                    html.Span('1000€', id='value-value'),
                ], className='value-container'),
                html.Div([
                    html.H4('Liquidity'),
                    html.Span('1066,66€', id='liquidity-value'),
                ], className='liquidity-container'),
            ], className='stats-container'),
        ], className='rebalancing-and-stats-container'),
        dcc.Graph(id='portfolio-graph'),
        html.Button(id='rebalance-button',
                    children=[
                        'Rebalance', 
                    ]),
    ], className='container')
