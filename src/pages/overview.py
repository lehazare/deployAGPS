from dash import dcc, html
from pages.utils import Header

def create_layout(app):
    return html.Div([
        Header(app),

        html.H2("KANJI 90"),
        
        html.P("The objective of this application is to assist the manager of a structured product in their daily tasks."),
        html.P(
            "The objective of management of the OPCVM is to allow the investor, holder of shares of the OPCVM at 'date T0', to receive at the maturity of the formula, at 'date Tc', 80% of their initial investment (€1000) excluding entry fees, increased by 100% of the Final Average Performance of a Basket of Indices composed of the Euro Stoxx 50, the Hang Seng, and the Standard & Poor's 500."
        ),
        html.P(
            "The Performances of each Index of the Basket are calculated annually on dates 'date T1' to 'date Tc', relative to their Initial Level on 'date T0', and are retained for their real value in the calculation of the Average Performance of the Basket."
        ),
        html.P(
            "The Performances of the Basket are also calculated annually, on dates 'date T1' to 'date Tc', and are obtained by taking the arithmetic average of the Performances of the previously calculated Indices. If an Average Performance is negative, it will be replaced by zero."
        ),
        html.P(
            "The Final Average Performance of the Basket is obtained by taking the arithmetic average of the Performances of the Basket that have thus been retained."
        ),
        html.P(
            "In addition, on each of the dates 'date T1' to 'date Tc', if the Performance of the Basket is positive, an amount equal to: - €30 if the Performance of the Basket is greater than or equal to 3%, or - €1000 x Performance of the Basket (€) if the Performance of the Basket is between 0 and 3%, will be paid to the purchaser. If the Performance of the Basket is negative, nothing will be paid to the purchaser."
        ),
    ], className='container')
