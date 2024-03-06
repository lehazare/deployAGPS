import plotly.graph_objs as go
from datetime import datetime
import pandas as pd

def plot_market(df, selected_set, current_date):
    # Sélectionner les colonnes "S&P500", "HANGSENG" & "EUROSTOXX50" pour l'ensemble sélectionné
    selected_columns = ["Date", "EUROSTOXX50", "SP500", "HANGSENG"]
    selected_data = df[selected_columns].copy()

    # Convertir la colonne "Date" en objets date Python
    selected_data["Date"] = pd.to_datetime(selected_data["Date"]).dt.date

    # Assurer que selected_set['T0'] et selected_set['Tc'] sont des objets date Python
    selected_set['T0'] = datetime.strptime(selected_set['T0'].strftime("%m/%d/%Y"), "%m/%d/%Y").date()
    current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
    
    # Filtrer les données en fonction de T0 et Tc de l'ensemble sélectionné
    selected_data = selected_data[ (selected_data["Date"] <= current_date)]

    # Créer une figure pour chaque graphique
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()

    # Ajouter les traces pour chaque colonne sélectionnée
    fig1.add_trace(go.Scatter(x=selected_data["Date"], y=selected_data["EUROSTOXX50"], mode='lines', name='EUROSTOXX50', line=dict(color='#007bff')))
    fig2.add_trace(go.Scatter(x=selected_data["Date"], y=selected_data["SP500"], mode='lines', name='S&P500', line=dict(color='red')))
    fig3.add_trace(go.Scatter(x=selected_data["Date"], y=selected_data["HANGSENG"], mode='lines', name='HANGSENG', line=dict(color='green')))

    # Ajouter des lignes verticales
    fig1.add_vline(x=selected_set["T0"], line_width=3, line_dash="dash", line_color="green")
    fig2.add_vline(x=selected_set["T0"], line_width=3, line_dash="dash", line_color="green")
    fig3.add_vline(x=selected_set["T0"], line_width=3, line_dash="dash", line_color="green")

    fig1.add_vline(x=selected_set["T1"], line_width=3, line_dash="dash", line_color="purple")
    fig2.add_vline(x=selected_set["T1"], line_width=3, line_dash="dash", line_color="purple")
    fig3.add_vline(x=selected_set["T1"], line_width=3, line_dash="dash", line_color="purple")

    fig1.add_vline(x=selected_set["T2"], line_width=3, line_dash="dash", line_color="purple")
    fig2.add_vline(x=selected_set["T2"], line_width=3, line_dash="dash", line_color="purple")
    fig3.add_vline(x=selected_set["T2"], line_width=3, line_dash="dash", line_color="purple")

    fig1.add_vline(x=selected_set["T3"], line_width=3, line_dash="dash", line_color="purple")
    fig2.add_vline(x=selected_set["T3"], line_width=3, line_dash="dash", line_color="purple")
    fig3.add_vline(x=selected_set["T3"], line_width=3, line_dash="dash", line_color="purple")

    fig1.add_vline(x=selected_set["T4"], line_width=3, line_dash="dash", line_color="purple")
    fig2.add_vline(x=selected_set["T4"], line_width=3, line_dash="dash", line_color="purple")
    fig3.add_vline(x=selected_set["T4"], line_width=3, line_dash="dash", line_color="purple")

    fig1.add_vline(x=selected_set["Tc"], line_width=3, line_dash="dash", line_color="red")
    fig2.add_vline(x=selected_set["Tc"], line_width=3, line_dash="dash", line_color="red")
    fig3.add_vline(x=selected_set["Tc"], line_width=3, line_dash="dash", line_color="red")

    fig1.add_vline(x=current_date, line_width=3, line_dash="dash", line_color="black")
    fig2.add_vline(x=current_date, line_width=3, line_dash="dash", line_color="black")
    fig3.add_vline(x=current_date, line_width=3, line_dash="dash", line_color="black")

    # Ajouter des annotations
    fig1.add_annotation(x=selected_set["T0"], text="T0")
    fig1.add_annotation(x=selected_set["T1"], text="T1")
    fig1.add_annotation(x=selected_set["T2"], text="T2")
    fig1.add_annotation(x=selected_set["T3"], text="T3")
    fig1.add_annotation(x=selected_set["T4"], text="T4")
    fig1.add_annotation(x=selected_set["Tc"], text="Tc")
    fig1.add_annotation(x=current_date, text="Current Date", yshift=25)

    fig2.add_annotation(x=selected_set["T0"], text="T0")
    fig2.add_annotation(x=selected_set["T1"], text="T1")
    fig2.add_annotation(x=selected_set["T2"], text="T2")
    fig2.add_annotation(x=selected_set["T3"], text="T3")
    fig2.add_annotation(x=selected_set["T4"], text="T4")
    fig2.add_annotation(x=selected_set["Tc"], text="Tc")
    fig2.add_annotation(x=current_date, text="Current Date", yshift=25)

    fig3.add_annotation(x=selected_set["T0"], text="T0")
    fig3.add_annotation(x=selected_set["T1"], text="T1")
    fig3.add_annotation(x=selected_set["T2"], text="T2")
    fig3.add_annotation(x=selected_set["T3"], text="T3")
    fig3.add_annotation(x=selected_set["T4"], text="T4")
    fig3.add_annotation(x=selected_set["Tc"], text="Tc")
    fig3.add_annotation(x=current_date, text="Current Date", yshift=25)

    # Mise en forme des graphiques
    fig1.update_layout(title='EUROSTOXX50', xaxis_title='Date', yaxis_title='Value in €')
    fig2.update_layout(title='S&P500', xaxis_title='Date', yaxis_title='Value in $')
    fig3.update_layout(title='HANGSENG', xaxis_title='Date', yaxis_title='Value in HKD')

    return fig1, fig2, fig3


def plot_portfolio(df_portfolio, df_market, selected_set, current_date, n_clicks):
    fig = go.Figure()
    if n_clicks is not None:
        # Sélectionner les colonnes "S&P500", "HANGSENG" & "EUROSTOXX50" pour l'ensemble sélectionné
        selected_columns = ["Date"]
        selected_data = df_market[selected_columns].copy()

        # Convertir la colonne "Date" en objets date Python
        selected_data["Date"] = pd.to_datetime(selected_data["Date"]).dt.date

        # Assurer que selected_set['T0'] et selected_set['Tc'] sont des objets date Python
        selected_set['T0'] = datetime.strptime(selected_set['T0'].strftime("%m/%d/%Y"), "%m/%d/%Y").date()
        selected_set['Tc'] = datetime.strptime(selected_set['Tc'].strftime("%m/%d/%Y"), "%m/%d/%Y").date()
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
        
        # Filtrer les données en fonction de T0 et Tc de l'ensemble sélectionné
        selected_data = selected_data[ (selected_data["Date"] <= selected_set['Tc']) & (selected_data["Date"] >= selected_set['T0'])]
        
        #reset index
        selected_data = selected_data.reset_index(drop=True)
        
        # Merge df_portfolio and selected_data on the index
        df_portfolio = df_portfolio.merge(selected_data, left_index=True, right_index=True)

        fig.add_trace(go.Scatter(x=df_portfolio['Date'], y=df_portfolio['price'], mode='lines', name='Portfolio', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df_portfolio['Date'], y=df_portfolio['value'], mode='lines', name='Value', line=dict(color='red')))

        fig.add_vline(x=selected_set["T0"], line_width=3, line_dash="dash", line_color="green")
        fig.add_vline(x=selected_set["T1"], line_width=3, line_dash="dash", line_color="purple")
        fig.add_vline(x=selected_set["T2"], line_width=3, line_dash="dash", line_color="purple")
        fig.add_vline(x=selected_set["T3"], line_width=3, line_dash="dash", line_color="purple")
        fig.add_vline(x=selected_set["T4"], line_width=3, line_dash="dash", line_color="purple")
        fig.add_vline(x=selected_set["Tc"], line_width=3, line_dash="dash", line_color="red")
        fig.add_vline(x=current_date, line_width=3, line_dash="dash", line_color="black")

        fig.add_annotation(x=selected_set["T0"], text="T0")
        fig.add_annotation(x=selected_set["T1"], text="T1")
        fig.add_annotation(x=selected_set["T2"], text="T2")
        fig.add_annotation(x=selected_set["T3"], text="T3")
        fig.add_annotation(x=selected_set["T4"], text="T4")
        fig.add_annotation(x=selected_set["Tc"], text="Tc")
        fig.add_annotation(x=current_date, text="Current Date")

        fig.update_layout(title='Portfolio', xaxis_title='Date', yaxis_title='Value in €')
    return fig