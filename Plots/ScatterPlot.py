
from pandas.core.arrays import categorical
from DashApp import app
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


@app.callback(Output("scatter-plot-matrix-color", "options"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def scatter_plot_matrix_color(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if len(combinedList) > 0:
        return [{"label": i, "value": i} for i in combinedList]
    else:
        return []

@app.callback(Output("Scatter-plot-matrix", "figure"), 
             Input("results-data-upload", "children"), Input("scatter-plot-matrix-color", "value"),
             Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_scatter_plot(jsonified_df, colorVariable, dependentVarList, independentVarList):
    dimensions = independentVarList + dependentVarList
    if (colorVariable is not None):
        dimensions.remove(colorVariable)
    if ((jsonified_df is not None) and (len(dimensions) > 2)):
        df = pd.read_json(jsonified_df)
        combinedList = independentVarList + dependentVarList
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]
        fig = px.scatter_matrix(variableDataFrame, dimensions=dimensions, color=colorVariable)
        return fig
    else:
        return {}