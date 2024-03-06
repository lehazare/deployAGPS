from dash import dcc, html, dash_table

from pages.utils import Header, Dates

def create_layout(app):
    return html.Div([
        Header(app),
        Dates(app),
        html.Div([
            html.Div([
                html.H4('EUROSTOXX50'),
                dash_table.DataTable(id='table1',
                                     style_cell={'background-color': '#007bff',
                                             'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                                             'textAlign': 'center',
                                             },
                                 style_header={'fontWeight': 'bold'},
                                 cell_selectable = False,
                                 style_cell_conditional=[
                                     {
                                         'if': {'column_id': c},
                                         'fontWeight': 'bold'
                                     } for c in ['Performances']
                                 ],
                                 style_as_list_view=True),
            ], className='table-container1'),
            html.Div([
                html.H4('S&P500'),
                dash_table.DataTable(id='table2',
                                     style_cell={'background-color': 'red',
                                             'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                                             'text_align': 'center'},
                                 style_header={'fontWeight': 'bold'},
                                 cell_selectable = False,
                                 style_cell_conditional=[
                                     {
                                         'if': {'column_id': c},
                                         'fontWeight': 'bold'
                                     } for c in ['Performances']
                                 ],
                                 style_as_list_view=True
                                     ),
            ], className='table-container2'),
            html.Div([
                html.H4('HANGSENG'),
                dash_table.DataTable(id='table3',
                                     style_cell={'background-color': 'green',
                                             'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                                             'text_align': 'center'},
                                 style_header={'fontWeight': 'bold'},
                                 cell_selectable = False,
                                 style_cell_conditional=[
                                     {
                                         'if': {'column_id': c},
                                         'fontWeight': 'bold'
                                     } for c in ['Performances']
                                 ],
                                 style_as_list_view=True),
            ], className='table-container3'),
        ] , className='full-tables-container'),      
        dcc.Graph(id='graph1'), 
        dcc.Graph(id='graph2'),  
        dcc.Graph(id='graph3'),      
        html.Button('Generate the Output', id='generate-csv-button'),
        html.Div(id='output-answer'),
    ], className='container')