from DashApp import app
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@app.callback(Output("Box-plot", "figure"), 
             Input("results-data-upload", "children"),
             Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_box_plot(jsonified_df, dependentVarList, independentVarList):
    combinedList = independentVarList + dependentVarList
    if ((jsonified_df is not None) and (len(combinedList) > 0)):
        df = pd.read_json(jsonified_df)
        variableDataFrame = df[[c for c in df.columns if c in combinedList]]
        fig = make_subplots(rows=1, cols=len(combinedList), subplot_titles=combinedList, y_title="Values")
        for i in range(len(combinedList)):
            fig.add_trace(go.Box(y=variableDataFrame[combinedList[i]], name=combinedList[i]), row=1, col=i+1)
        return fig
    else:
        return {}