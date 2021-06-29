
from DashApp import app
from dash.dependencies import Input, Output
import SensitivityAnalysis as sa
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

@app.callback(Output("Delta-analysis-results", "figure"), 
             Input("results-data-upload", "children"),
             Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_delta_graph(jsonified_df, dependentVarList, independentVarList):
    if ((jsonified_df is not None) and (dependentVarList) and (independentVarList)):
        df = pd.read_json(jsonified_df)
        deltaResult = sa.DeltaSensitivityAnalysis(df, independentVarList, dependentVarList)
        fig = make_subplots(rows=1, cols=len(dependentVarList), subplot_titles=["Delta sensitivity index for " + c for c in dependentVarList], y_title="Sensitivity Index")
        for i in range(len(dependentVarList)):
            deltaResultDF = pd.DataFrame.from_dict(deltaResult[i])
            fig.add_trace(go.Bar(name = "S1", x= independentVarList, y= deltaResultDF["S1"], error_y=dict(type="data", array=deltaResultDF["S1_conf"])), row=1, col= i+1)
            fig.add_trace(go.Bar(name = "delta", x= independentVarList, y= deltaResultDF["delta"], error_y=dict(type="data", array=deltaResultDF["delta_conf"])), row=1, col= i+1)
        return fig
    else:
        return {}