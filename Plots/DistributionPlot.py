from DashApp import app
from dash.dependencies import Input, Output
import pandas as pd
import plotly.figure_factory as ff
import numpy as np


@app.callback(Output("Distribution-plot", "figure"), 
             Input("results-data-upload", "children"),
             Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_distribution_plot(jsonified_df, dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    #combinedList = list(set(combinedList))
    if ((jsonified_df is not None) and (len(combinedList) > 0)):
        df = pd.read_json(jsonified_df)
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]
        fig = ff.create_distplot(np.transpose(variableDataFrame.to_numpy()), variableDataFrame.columns.values.tolist())
        return fig
    else:
        return {}