from DashApp import app
from dash.dependencies import Input, Output
from sklearn.decomposition import PCA
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

@app.callback(Output("pca-colorscale", "options"), Output("pca-colorscale", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def pca_colorscale_list(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if len(combinedList) > 0:
        return [{"label": i, "value": i} for i in combinedList], combinedList[0]
    else:
        return [], None


@app.callback(Output("PCA-plot", "figure"),
              Input("results-data-upload", "children"), Input("pca-slider", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"),
              Input("pca-colorscale", "value"))
def update_pca_plot(jsonified_df, n_components, dependentVarList, independentVarList, colorScaleVariable):
    combinedList = independentVarList + dependentVarList
    if ((jsonified_df is not None) and (independentVarList) and (dependentVarList) and colorScaleVariable is not None):
        pca = PCA(n_components = n_components)
        df = pd.read_json(jsonified_df)
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]

        components = pca.fit_transform(variableDataFrame)
        var = pca.explained_variance_ratio_.sum()*100
        
        labels = {str(i): f"PC {i+1} ({var:.1f}%)" for i,var in enumerate(pca.explained_variance_ratio_*100)}
        labels["color"] = colorScaleVariable

        fig = px.scatter_matrix(components, dimensions=range(n_components), color = variableDataFrame[colorScaleVariable],
                                labels=labels, title=f"PCA Analysis: Total Explained Variable: {var:.2f}%")
        
        fig.update_traces(diagonal_visible = False)
        return fig
    else:
        return {}


@app.callback(Output("PCA-Loadings-plot", "figure"),
              Input("results-data-upload", "children"), Input("pca-slider", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_pca_loadings_plot(jsonified_df, n_components, dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if ((jsonified_df is not None) and (independentVarList) and (dependentVarList)):
        pca = PCA(n_components = n_components)
        df = pd.read_json(jsonified_df)
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]

        components = pca.fit_transform(variableDataFrame)
        loadings= pca.components_.T * np.sqrt(pca.explained_variance_)
        subplot_titles = ["PC " + str(i+1) + "(" + f"{var:.1f}" + "%)" for i,var in enumerate(pca.explained_variance_ratio_*100)]

        fig = make_subplots(rows=1, cols=n_components, subplot_titles=subplot_titles, y_title="Loading")
        for i in range(n_components):
            fig.add_trace(go.Bar(x=combinedList, y=np.transpose(loadings)[i], showlegend=False), row=1, col=i+1)

        return fig
    else:
        return {}