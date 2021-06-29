from DashApp import app
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

@app.callback(Output("manova-view", "children"), Input("manova-type-dropdown", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_manova_view(manovaType, depVarList, indepVarList):
    combinedList = depVarList + indepVarList
    if combinedList is not None:
        if manovaType == "one-way-manova":
            return html.Div(children=[
                dcc.Dropdown(id="manova-oneway-indep-1", options=[{"label": i, "value": i} for i in combinedList], 
                   placeholder="Select independent variable (categorical)", multi=False),
                dcc.Dropdown(id="manova-oneway-dep-1", options=[{"label": i, "value": i} for i in combinedList],
                   placeholder="Select dependent variables (continuous)", multi=True)])
        elif manovaType == "two-way-manova":
            return html.Div(children=[
                dcc.Dropdown(id="manova-twoway-indep-1", options=[{"label": i, "value": i} for i in combinedList],
                    placeholder="Select independent variable 1 (categorical)", multi=False),
                dcc.Dropdown(id="manova-twoway-indep-2", options=[{"label": i, "value": i} for i in combinedList],
                    placeholder="Select independent variable 2 (categorical)", multi=False),
                dcc.Dropdown(id="manova-twoway-dep-1", options=[{"label": i, "value":i} for i in combinedList],
                    placeholder="Select dependent variables (continuous)", multi=True)])
    else:
        return []


@app.callback(Output("manova-results", "children"), Input("manova-type-dropdown", "value"))
def render_manova_results(manovaType):
    if manovaType is not None:
        if manovaType == "one-way-manova":
            return html.Div(id="one-way-manova-results")
        elif manovaType == "two-way-manova":
            return html.Div(id="two-way-manova-results")
    else:
        return {}

@app.callback(Output("one-way-manova-results", "children"), Input("results-data-upload", "children"),
              Input("manova-oneway-indep-1", "value"), Input("manova-oneway-dep-1", "value"))
def update_one_way_manova_results(jsonified_df, manovaOneWayIndep1, manovaOneWayDepValues):
    return {}

@app.callback(Output("two-way-manova-results", "children"), Input("results-data-upload", "children"),
              Input("manova-twoway-indep-1", "value"), Input("manova-twoway-indep-2", "value"),
              Input("manova-twoway-dep-1", "value"))
def update_two_way_manova_results(jsonified_df, manovaTwoWayIndep1, manovaTwoWayIndep2, manovaTwoWayDep1):
    return {}

@app.callback(Output("mancova-view", "children"), Input("mancova-type-dropdown", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_mancova_view(mancovaType, depVarList, indepVarList):
    combinedList = depVarList + indepVarList
    if combinedList is not None:
        if mancovaType == "one-way-mancova":
            return html.Div(children=[
                dcc.Dropdown(id="mancova-oneway-indep-1", options=[{"label": i, "value": i} for i in combinedList], 
                   placeholder="Select independent variable (categorical)", multi=False),
                dcc.Dropdown(id="mancova-oneway-covariate-1",  options=[{"label": i, "value": i} for i in combinedList],
                   placeholder="Select independent variable (continuous)", multi=False),
                dcc.Dropdown(id="mancova-oneway-dep-1", options=[{"label": i, "value": i} for i in combinedList],
                   placeholder="Select dependent variables (continuous)", multi=True)])
        if mancovaType == "two-way-mancova":
            return html.Div(children=[
                dcc.Dropdown(id="mancova-twoway-indep-1", options=[{"label": i, "value": i} for i in combinedList], 
                   placeholder="Select independent variable 1 (categorical)", multi=False),
                dcc.Dropdown(id="mancova-twoway-indep-2", options=[{"label": i, "value": i} for i in combinedList], 
                   placeholder="Select independent variable 2 (categorical)", multi=False),
                dcc.Dropdown(id="mancova-twoway-covariate-1",  options=[{"label": i, "value": i} for i in combinedList],
                   placeholder="Select independent variable (continuous)", multi=False),
                dcc.Dropdown(id="mancova-twoway-dep-1", options=[{"label": i, "value": i} for i in combinedList],
                   placeholder="Select dependent variables (continuous)", multi=True)])
    else:
        return []

@app.callback(Output("mancova-results", "children"), Input("mancova-type-dropdown", "value"))
def render_mancova_results(mancovaType):
    if mancovaType is not None:
        if mancovaType == "one-way-mancova-results":
            return html.Div(id="one-way-mancova-results")
        elif mancovaType == "two-way-mancova-results":
            return html.Div(id="two-way-mancova-results")
    else:
        return {} 

@app.callback(Output("one-way-mancova-results", "children"), Input("results-data-upload", "children"),
              Input("mancova-oneway-indep-1", "value"), Input("mancova-oneway-covariate-1", "value"),
              Input("mancova-oneway-dep-1", "value"))
def update_one_way_mancova_results(jsonified_df, mancovaOneWayIndep1, mancovaOneWayCovariate1, mancovaOneWayDeps):
    return {}

@app.callback(Output("two-way-mancova-results", "children"), Input("results-data-upload", "children"),
              Input("mancova-twoway-indep-1", "value"), Input("mancova-twoway-indep-2", "value"),
              Input("mancova-twoway-covariate-1", "value"), Input("mancova-twoway-dep-1", "value"))
def update_two_way_mancova_results(jsonified_df, mancovaTwoWayIndep1, mancovaTwoWayIndep2, mancovaTwoWayCovariate1, mancovaTwoWayDeps):
    return {}       