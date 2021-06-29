from DashApp import app
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

@app.callback(Output("3d-x-axis-var", "options"), Output("3d-x-axis-var", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_3d_xVar_list(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if len(combinedList) > 0:
        return [{"label": i, "value": i} for i in combinedList], combinedList[0]
    else:
        return [], None

@app.callback(Output("3d-y-axis-var", "options"), Output("3d-y-axis-var", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_3d_yVar_list(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if  len(combinedList) > 1:
        return [{"label": i, "value": i} for i in combinedList], combinedList[1]
    else:
        return [], None

@app.callback(Output("3d-z-axis-var", "options"), Output("3d-z-axis-var", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_3d_zVar_list(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if  len(combinedList) > 2:
        return [{"label": i, "value": i} for i in combinedList], combinedList[2]
    else:
        return [], None

@app.callback(Output("3d-graph-color-scale", "options"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def graph_3d_plot_color_scale_dropdown(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if len(combinedList) > 3:
        return [{"label": i, "value": i} for i in combinedList]
    else:
        return []

@app.callback(Output("3d-graph", "figure"), Input("results-data-upload", "children"),
              Input("3d-x-axis-var", "value"), Input("3d-y-axis-var", "value"), Input("3d-z-axis-var", "value"),
              Input("3d-graph-color-scale", "value"))
def update_3d_graph(jsonified_df, xAxisVar, yAxisVar, zAxisVar, colorVariable):
    if jsonified_df is not None and xAxisVar is not None and yAxisVar is not None and zAxisVar is not None:
        df = pd.read_json(jsonified_df)
        fig = px.scatter_3d(df, x=xAxisVar, y=yAxisVar, z=zAxisVar, color=colorVariable)
        return fig
    else:
        return {}