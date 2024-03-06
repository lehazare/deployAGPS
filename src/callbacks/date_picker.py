# date_picker.py
import pandas as pd
from dash import Input, Output, State, ctx
from data.kanji90 import set1, set2, set3
from datetime import datetime, timedelta

# Callback to update min and max dates of DatePickerSingle based on dropdown value
def update_date_picker_callback(app, close_price_df):
    @app.callback(
        Output('my-date-picker-single', 'min_date_allowed'),
        Output('my-date-picker-single', 'max_date_allowed'),
        Output('my-date-picker-single', 'initial_visible_month'),
        Output('my-date-picker-single', 'date'),
        Output('date-set-dropdown', 'value'),
        Output('confirm-date', 'displayed'),
        Output('memory', 'data'),
        Input('date-set-dropdown', 'value'),
        Input('add_day', 'n_clicks'),
        Input('my-date-picker-single', 'date'),
        State('memory', 'data'),
    )
    def update_date_picker(selected_set, n_clicks, date, data):
        triggered_id = ctx.triggered_id
        displayed = False

        if data is None:
            data = {
                'min_date_allowed': '2000-07-05',
                'max_date_allowed': '2005-07-05',
                'initial_visible_month': '2000-07-05',
                'date': '2000-07-05',
                'selected_set': 'set1'
            }

        dates = close_price_df["Date"].copy()
        dates = pd.to_datetime(dates).dt.date

        if triggered_id == 'add_day':
            if n_clicks is not None:
                data['date'] = datetime.strptime(data['date'], "%Y-%m-%d").date()
                index = dates[dates == data['date']].index[0]
                date = dates[index + 1]
                data['date'] = date
            
        elif triggered_id == 'date-set-dropdown':
            if selected_set == 'set1':
                data['min_date_allowed'] = set1['T0']
                data['max_date_allowed'] = set1['Tc']
                data['initial_visible_month'] = set1['T0']
                data['date'] = set1['T0']
                data['selected_set'] = 'set1'
            elif selected_set == 'set2':
                data['min_date_allowed'] = set2['T0']
                data['max_date_allowed'] = set2['Tc']
                data['initial_visible_month'] = set2['T0']
                data['date'] = set2['T0']
                data['selected_set'] = 'set2'
            elif selected_set == 'set3':
                data['min_date_allowed'] = set3['T0']
                data['max_date_allowed'] = set3['Tc']
                data['initial_visible_month'] = set3['T0']
                data['date'] = set3['T0']
                data['selected_set'] = 'set3'
        elif triggered_id == 'my-date-picker-single':
            if date is not None:
                date = pd.to_datetime(date).date()
                if date in dates.values:
                    data['date'] = date
                else:
                    displayed = True

        return data['min_date_allowed'], data['max_date_allowed'], data['initial_visible_month'], data['date'], data['selected_set'], displayed, data


