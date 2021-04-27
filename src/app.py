# Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pycaret.regression import predict_model
from functions.data_prep import initialize_data, initialize_model

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_temp, new_df = initialize_data("data/benchmarks.csv")
saved_lr = initialize_model("model/FinalLr")

app.layout = html.Div(children=[
    html.H1(children="Payment Analytics", style={"textAlign": "center"}),
    html.Div(
        html.P(children="Select the year on the slider to see the total summed payments for each month. Analytics below are based on inputs. The defualt input is the previous year, but you are welcome to put any inputs you want into the linear regression model. Clicking on the year on the slider bar will populate the input boxes with that year\'s values.", style={"textAlign": "center"})
    ),
    dcc.Graph(
        figure = dict(
            data = [dict(x = df_temp.index, y = df_temp["PayAmt"].values, name = "year_payments",type = 'bar')],
            layout = dict(title = "Payments")
        ),
        id = "Payments"
    ),
    dcc.Slider(
        id="year-slider",
        min=df_temp.index.year.min(),
        max=df_temp.index.year.max(),
        value=df_temp.index.year.min(),
        marks={str(year): str(year) for year in df_temp.index.year.unique()},
        step=None
    ),
    html.Hr(),
    html.Div(children = [
        html.Div([html.P('January', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='January', value=78140.41, type='number')]),
        html.Div([html.P('Febuary', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='Febuary', value=65835.61, type='number')]),
        html.Div([html.P('March', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='March', value=55124.61, type='number')]),
        html.Div([html.P('April', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='April', value=21248.25, type='number')]),
        html.Div([html.P('May', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='May', value=21092.66, type='number')]),
        html.Div([html.P('June', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='June', value=38512.40, type='number')]),
        html.Div([html.P('July', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='July', value=57669.00, type='number')]),
        html.Div([html.P('August', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='August', value=52108.37, type='number')]),
        html.Div([html.P('September', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='September', value=79124.97, type='number')]),
        html.Div([html.P('October', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='October', value=68234.54, type='number')]),
        html.Div([html.P('November', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='November', value=42059.45, type='number')]),
        html.Div([html.P('December', style={"height": "auto", "margin-bottom": "auto"}), dcc.Input(id='December', value=30586.77, type='number')])
        ],
        style=dict(display='flex', flexWrap='wrap', width=800)
    ),
    dcc.Graph(
        figure = dict(
            data = [dict(x = new_df.index, y = new_df["Total"].values, name = "year_totals",type = 'bar')],
            layout = dict(title = "Totals with Prediction")
        ),
        id = "Yearly Totals"
    ),
])


@app.callback(
    Output('Payments', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df_temp[df_temp.index.year == selected_year]
    fig = dict(data = [dict(x = filtered_df.index, y = filtered_df["PayAmt"].values, name = "year_payments",type = 'bar')], layout = dict(title = "Payments"))
    return fig

@app.callback(
    Output('Yearly Totals', 'figure'),
    Input('January', 'value'),
    Input('Febuary', 'value'),
    Input('March', 'value'),
    Input('April', 'value'),
    Input('May', 'value'),
    Input('June', 'value'),
    Input('July', 'value'),
    Input('August', 'value'),
    Input('September', 'value'),
    Input('October', 'value'),
    Input('November', 'value'),
    Input('December', 'value'))
def update_figure_2(val1,val2,val3,val4,val5,val6,val7,val8,val9,val10,val11,val12):
    data_unseen = pd.DataFrame([[val1,val2,val3,val4,val5,val6,val7,val8,val9,val10,val11,val12]],columns = ["1","2","3","4","5","6","7","8","9","10","11","12"])
    new_prediction = predict_model(saved_lr, data=data_unseen)
    new_prediction["Total"] = new_prediction["Label"]
    new_prediction = new_prediction.drop(columns = ["Label"])
    pred_df = new_df.append(new_prediction)
    pred_df = pred_df.rename(index={0: 2021})
    pred_df['color'] = 'orange'
    pred_df['color'][:-1] = 'green'
    fig2 = dict(data = [dict(x = pred_df.index, y = pred_df["Total"].values, name = "year_totals",type = 'bar', marker={'color': pred_df['color']})], layout = dict(title = "Totals with Prediction"))
    return fig2
    
@app.callback(
    Output('January', 'value'),
    Output('Febuary', 'value'),
    Output('March', 'value'),
    Output('April', 'value'),
    Output('May', 'value'),
    Output('June', 'value'),
    Output('July', 'value'),
    Output('August', 'value'),
    Output('September', 'value'),
    Output('October', 'value'),
    Output('November', 'value'),
    Output('December', 'value'),
    Input('year-slider', 'value'))
def fill_inputs(year):
    inputs = df_temp[df_temp.index.year == year]["PayAmt"].values
    if len(inputs) != 12:
        inputs = df_temp[df_temp.index.year == 2020]["PayAmt"].values.round(2)

    return inputs[0],inputs[1],inputs[2],inputs[3],inputs[4],inputs[5],inputs[6],inputs[7],inputs[8],inputs[9],inputs[10],inputs[11]

if __name__ == '__main__':
    app.run_server(port=8000, host='127.0.0.1', debug=True)
