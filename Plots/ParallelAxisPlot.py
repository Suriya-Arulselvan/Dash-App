from DashApp import app
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

@app.callback(Output("parallel-colorscale", "options"), Output("parallel-colorscale", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def parallel_axis_colorscale_list(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if len(combinedList) > 0:
        return [{"label": i, "value": i} for i in combinedList], combinedList[0]
    else:
        return [], None

@app.callback(Output("Parallel-axis-diagram", "figure"), 
             Input("results-data-upload", "children"),
             Input("dependent-var-list", "children"), Input("independent-var-list", "children"),
             Input("parallel-colorscale", "value"))
def update_parallel_axis(jsonified_df, dependentVarList, independentVarList, colorScaleVariable):
    if ((jsonified_df is not None) and (dependentVarList) and (independentVarList)):
        df = pd.read_json(jsonified_df)
        combinedList = independentVarList + dependentVarList
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]
        fig = px.parallel_coordinates(variableDataFrame, color=colorScaleVariable, labels=variableDataFrame.columns.values.tolist(), 
                                        color_continuous_scale=px.colors.sequential.Electric)
        return fig
    else:
        return {}