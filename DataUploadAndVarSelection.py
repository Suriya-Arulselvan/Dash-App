import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from DashApp import app
import base64
import io
import os
import pandas as pd
import json
from dataprep.eda import create_report

def parse_content(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
            return df
    except Exception as e:
        print(e)
        return html.Div(['An exception occured in processing the file'])
    return json.loads('')


@app.callback(Output('results-data-upload', 'children'), Input('upload-data', 'contents'), 
              State('upload-data', 'filename'), State('upload-data', 'last_modified'))
def update_data(contents, filename, last_modified):
    if contents is not None:
        resultsDataFrame = parse_content(contents, filename, last_modified)
        return resultsDataFrame.to_json()

@app.callback(Output("download-report", "data"), Input("generate-report", "n_clicks"), 
              Input("results-data-upload","children"))
def generate_report(n_clicks, jsonified_df):
    if jsonified_df is not None:
        df = pd.read_json(jsonified_df)
        report = create_report(df)
        report.save(filename="report", to= os.getcwd() + "/Reports")
    return 


@app.callback(Output("variable-list", "children"), Input("results-data-upload", "children"))
def update_variable_list(jsonified_data):
    if jsonified_data is not None:
        dff = pd.read_json(jsonified_data)
        varList = dff.columns.values.tolist()
        varList.pop(0)
        return varList
    else:
        []

@app.callback(Output('independent-var-dropdown', 'options'), 
              Input('variable-list', 'children'), Input("dependent-var-list", "children"))
def get_independentVar_list(variable_list, dependentVar_list):
    if variable_list is not None:
        return [{'label': i, 'value': i} for i in variable_list if i not in dependentVar_list]
    else:
        return []

@app.callback(Output('dependent-var-dropdown', 'options'), 
              Input('variable-list', 'children'), Input("independent-var-list", "children"))
def get_dependentVar_list(variable_list, independentVar_list):
    if variable_list is not None:
        return [{'label': i, 'value': i} for i in variable_list if i not in independentVar_list]
    else:
        return []

@app.callback(Output("independent-var-list", "children"), Input("independent-var-dropdown", "value"))
def update_independentVar_list(values):
    if values is not None:
        return values
    else:
        return []

@app.callback(Output("dependent-var-list", "children"), Input("dependent-var-dropdown", "value"))
def update_dependentVar_list(values):
    if values is not None:
        return values
    else:
        return []
