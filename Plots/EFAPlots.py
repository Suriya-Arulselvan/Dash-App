
from plotly.subplots import make_subplots
from DashApp import app
from dash.dependencies import Input, Output
from factor_analyzer import FactorAnalyzer
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_table as dt
import numpy as np


@app.callback(Output("efa-scree-plot", "figure"),
              Input("results-data-upload", "children"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_efa_scree_plot(jsonified_df, dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if ((jsonified_df is not None) and (independentVarList) and (dependentVarList)):
        df = pd.read_json(jsonified_df)
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]

        fa = FactorAnalyzer(rotation=None)
        fa.fit(variableDataFrame)
        ev, v = fa.get_eigenvalues()

        fig = go.Figure(data=go.Scatter(x=list(range(1,25)), y=ev[:24]))
        fig.update_layout(title="Scree plot", xaxis_title="Factors", yaxis_title="Eigenvalue / variance ratio")
        return fig
    else:
        return {}

@app.callback(Output("fa-loading-radar-chart", "figure"),
              Input("results-data-upload", "children"), Input("efa-slider", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_fa_loading_radar_chart(jsonified_df, n_factors, dependentVarList, indpendentVarList):
    combinedList = indpendentVarList + dependentVarList
    if ((jsonified_df is not None) and indpendentVarList and dependentVarList):
        df = pd.read_json(jsonified_df)
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]

        fa = FactorAnalyzer(rotation="varimax", n_factors = n_factors, method="ml")
        fa.fit(variableDataFrame)

        categories = combinedList
        fig = go.Figure()

        for i in range(n_factors):
            fig.add_trace(go.Scatterpolar(r=np.transpose(fa.loadings_)[i], theta=categories, fill="toself", name= "Factor {0}".format(i)))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[-1, 1])), showlegend=True)

        return fig
    else:
        return {}


@app.callback(Output("fa-loading-table", "children"),
              Input("results-data-upload", "children"), Input("efa-slider", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_fa_loading_table(jsonified_df, n_factors, dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if ((jsonified_df is not None) and (independentVarList) and (dependentVarList)):
        df = pd.read_json(jsonified_df)
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]

        fa = FactorAnalyzer(rotation="varimax", n_factors = n_factors, method="ml")
        fa.fit(variableDataFrame)

        fa_loadingMatrix = pd.DataFrame(fa.loadings_, columns=["FA{}".format(i) for i in range(1, n_factors + 1)], index = variableDataFrame.columns)
        fa_loadingMatrix["Highest_loading"] = fa_loadingMatrix.idxmax(axis=1)
        fa_loadingMatrix = fa_loadingMatrix.sort_values("Highest_loading")
        
        data = fa_loadingMatrix.to_dict("rows")
        columns = [{"name": i, "id": i} for i in fa_loadingMatrix.columns]
        return dt.DataTable(data = data, columns = columns)
    else:
        return {}