from dash import html, dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])

def Dates(app):
    return html.Div([get_dates(app)])

def get_header(app):
    header = html.Div(
        [
        html.H1("Structured Products Manager"),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/",
                className="tab",
            ),
            dcc.Link(
                "Price Performance",
                href="/price-performance",
                className="tab",
            ),
            dcc.Link(
                "Portfolio & Management",
                href="/portfolio-management",
                className="tablast",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row.iloc[i]]))
        table.append(html.Tr(html_row))
    return table

def get_dates(app):
    dates = html.Div(
        [
            dcc.ConfirmDialog(
                id='confirm-date',
                message='At this date, the market is closed. Please select another date before doing anything else.',
            ),
            dcc.Dropdown(
            id='date-set-dropdown',
            options=[
                {'label': '2000 - 2005', 'value': 'set1'},
                {'label': '2005 - 2010', 'value': 'set2'},
                {'label': '2009 - 2014', 'value': 'set3'}
            ],
            className='container'
        ),
        html.Button('+1 Day', id='add_day'),
        dcc.DatePickerSingle(
            id='my-date-picker-single',
            className='container',
            display_format='DD/MM/Y',
        ),
        ],
        className="dates-container",
    )
    return dates
