from DashApp import app
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn import linear_model, tree, neighbors


models={"Linear Regression": linear_model.LinearRegression, 
        "Decision Tree": tree.DecisionTreeRegressor,
        "k-NN": neighbors.KNeighborsRegressor}

@app.callback(Output("2d-x-axis-var", "options"), Output("2d-x-axis-var", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_2d_xVar_list(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if len(combinedList) > 0:
        return [{"label": i, "value": i} for i in combinedList], combinedList[0]
    else:
        return [], None

@app.callback(Output("2d-y-axis-var", "options"), Output("2d-y-axis-var", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_2d_yVar_list(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if len(combinedList) > 1:
        return [{"label": i, "value": i} for i in combinedList], combinedList[1]
    else:
        return [], None

@app.callback(Output("2d-graph-color-scale", "options"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def graph_2d_plot_color_scale_dropdown(dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if len(combinedList) > 2:
        return [{"label": i, "value": i} for i in combinedList]
    else:
        return []

@app.callback(Output("2d-graph", "figure"), Input("results-data-upload", "children"),
              Input("2d-x-axis-var", "value"), Input("2d-y-axis-var", "value"), 
              Input("2d-graph-color-scale", "value"), Input("2d-regression-models", "value"))
def update_2d_graph(jsonified_df, xAxisVar, yAxisVar, colorVariable, regressionModel):
    if jsonified_df is not None and xAxisVar is not None and yAxisVar is not None:
        df = pd.read_json(jsonified_df)
        fig = px.scatter(df, x=xAxisVar, y=yAxisVar, color=colorVariable)
        if regressionModel is not None:
            global models
            model = models[regressionModel]()
            model.fit(df[xAxisVar].values.reshape(-1,1), df[yAxisVar])
            x_range = np.linspace(df[xAxisVar].min(), df[xAxisVar].max(), 100)
            y_range = model.predict(x_range.reshape(-1,1))
            fig.add_traces(go.Scatter(x=x_range, y=y_range, name="Prediction"))
        return fig
    else:
        return {}
