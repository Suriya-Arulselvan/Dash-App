
from DashApp import app
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import SensitivityAnalysis as sa
import pandas as pd
import plotly.graph_objects as go

@app.callback(Output("SOBOL-analysis-results", "figure"), 
             Input("results-data-upload", "children"),
             Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_sobol_graph(jsonified_df, dependentVarList, independentVarList):
    if ((jsonified_df is not None) and (dependentVarList) and (independentVarList)):
        df = pd.read_json(jsonified_df)
        sobolResult = sa.SobolSensitivityAnalysis(df, independentVarList, dependentVarList)
        fig = make_subplots(rows=1, cols=len(dependentVarList), subplot_titles=["Sobol sensitivity index for " + c for c in dependentVarList], y_title="Sensitivity Index")
        for i in range(len(dependentVarList)):
            #sobolResult[i].pop("S2")
            #sobolResult[i].pop("S2_conf")
            sobolResultDF = pd.DataFrame.from_dict(sobolResult[i])
            fig.add_trace(go.Bar(name = "S1", x= independentVarList, y= sobolResultDF["S1"], error_y=dict(type="data", array=sobolResultDF["S1_conf"])), row=1, col= i+1)
            fig.add_trace(go.Bar(name = "ST", x= independentVarList, y= sobolResultDF["ST"], error_y=dict(type="data", array=sobolResultDF["ST_conf"])), row=1, col= i+1)
        return fig
    else:
        return {}
