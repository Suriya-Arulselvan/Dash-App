from DashApp import app
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np


@app.callback(Output("Correlation-heatmap", "figure"), 
             Input("results-data-upload", "children"),
             Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_correlation_heatmap(jsonified_df, dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    combinedList = list(set(combinedList))
    if ((jsonified_df is not None) and (len(combinedList) > 2)):
        df = pd.read_json(jsonified_df)
        combinedList = independentVarList + dependentVarList
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]
        correlation = variableDataFrame.corr()
        fig = go.Figure(data=[go.Heatmap(z=correlation.values, x=correlation.index.values, y=correlation.columns.values)])
        return fig
    else:
        return {}