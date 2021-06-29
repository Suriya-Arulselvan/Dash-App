from DashApp import app
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt


@app.callback(Output("anova-view", "children"), Input("anova-type-dropdown", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_anova_view(anovaType, depVarList, indepVarList):
    combinedList = depVarList + indepVarList
    if combinedList is not None:
        if anovaType == "one-way-anova":
            return html.Div(children=[
                dcc.Dropdown(id="anova-oneway-indep-1", options=[{"label": i, "value": i} for i in combinedList], 
                   placeholder="Select independent variable (categorical)", multi=False),
                dcc.Dropdown(id="anova-oneway-dep-1", options=[{"label": i, "value": i} for i in combinedList],
                   placeholder="Select dependent variable (continuous)", multi=False)])
        elif anovaType == "two-way-anova":
            return html.Div(children=[
                dcc.Dropdown(id="anova-twoway-indep-1", options=[{"label": i, "value": i} for i in combinedList],
                    placeholder="Select independent variable 1 (categorical)", multi=False),
                dcc.Dropdown(id="anova-twoway-indep-2", options=[{"label": i, "value": i} for i in combinedList],
                    placeholder="Select independent variable 2 (categorical)", multi=False),
                dcc.Dropdown(id="anova-twoway-dep-1", options=[{"label": i, "value":i} for i in combinedList],
                    placeholder="Select dependent variable (continuous)", multi=False)
            ])
    else:
        return []

def anova_table(aov):
    aov['mean_sq'] = aov[:]['sum_sq']/aov[:]['df']
    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*aov['mean_sq'][-1]))/(sum(aov['sum_sq'])+aov['mean_sq'][-1])
    cols = ['sum_sq', 'df', 'mean_sq', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
    aov = aov[cols]
    return aov

@app.callback(Output("anova-results", "children"), Input("anova-type-dropdown", "value"))
def render_anova_results(anovaType):
    if anovaType is not None:
        if anovaType == "one-way-anova":
            return html.Div(id="one-way-anova-results")
        elif anovaType == "two-way-anova":
            return html.Div(id="two-way-anova-results")
    else:
        return {}

@app.callback(Output("one-way-anova-results", "children"),
              Input("results-data-upload", "children"),
              Input("anova-oneway-indep-1", "value"), Input("anova-oneway-dep-1", "value"))
def update_one_way_anova_results(jsonified_df, anovaOneWayIndep1, anovaOneWayDep1):
    if jsonified_df is not None:
        df = pd.read_json(jsonified_df)
        if anovaOneWayIndep1 is not None and anovaOneWayDep1 is not None:
            model = ols("{0} ~ C({1})".format(anovaOneWayDep1, anovaOneWayIndep1), data = df).fit()
            table = sm.stats.anova_lm(model, typ=2)
            aov = anova_table(table)
            columns = [{"name": i, "id": i} for i in aov.columns]
            return dt.DataTable(data = aov.to_dict("records"), columns=columns)
        else:
            return {}
    else:
        return {}

@app.callback(Output("two-way-anova-results", "children"), Input("results-data-upload", "children"), 
              Input("anova-twoway-indep-1", "value"), Input("anova-twoway-indep-2", "value"),
              Input("anova-twoway-dep-1", "value"))
def update_two_way_anova_results(jsonified_df, anovaTwoWayIndep1, anovaTwoWayIndep2, anovaTwoWayDep1):
    if jsonified_df is not None:
        df = pd.read_json(jsonified_df)
        if anovaTwoWayIndep1 is not None and anovaTwoWayIndep2 is not None and anovaTwoWayDep1 is not None:
            model = ols("{0} ~ C({1}) + C({2}) + C({1}):C({2})".format(anovaTwoWayDep1, anovaTwoWayIndep1, anovaTwoWayIndep2), data = df).fit()
            table= sm.stats.anova_lm(model, typ=2)
            columns = [{"name" : i, "id": i} for i in table.columns]
            return dt.DataTable(data = table.to_dict("records"), columns=columns)
        else:
            return {}
    else:
        return {}


@app.callback(Output("ancova-view", "children"), Input("ancova-type-dropdown", "value"),
              Input("dependent-var-list", "children"), Input("independent-var-list", "children"))
def update_ancova_view(ancovaType, depVarList, indepVarList):
    combinedList = depVarList + indepVarList
    if combinedList is not None:
        if ancovaType == "one-way-ancova":
            return html.Div(children=[
                dcc.Dropdown(id="ancova-oneway-indep-1", options=[{"label": i, "value": i} for i in combinedList],
                    placeholder="Select independent variable 1 (categorical)", multi=False),
                dcc.Dropdown(id="ancova-oneway-covariate-1", options=[{"label": i, "value": i} for i in combinedList],
                    placeholder="Select covariate variable (continuous)", multi=False),
                dcc.Dropdown(id="ancova-oneway-dep-1", options=[{"label": i, "value":i} for i in combinedList],
                    placeholder="Select dependent variable (continuous)", multi=False)])
        elif ancovaType == "two-way-ancova":
            return html.Div(children=[
                dcc.Dropdown(id="ancova-twoway-indep-1", options=[{"label": i, "value": i} for i in combinedList],
                    placeholder="Select independent variable 1 (categorical)", multi=False),
                dcc.Dropdown(id="ancova-twoway-indep-2", options=[{"label": i, "value": i} for i in combinedList],
                    placeholder="Select independent variable 2 (categorical)", multi=False),
                dcc.Dropdown(id="ancova-twoway-covariate-1", options=[{"label": i, "value": i} for i in combinedList],
                    placeholder="Select covariate variable (continuous)", multi=False),
                dcc.Dropdown(id="ancova-twoway-dep-1", options=[{"label": i, "value":i} for i in combinedList],
                    placeholder="Select dependent variable (continuous)", multi=False)])
    else:
        return []

@app.callback(Output("ancova-results", "children"), Input("ancova-type-dropdown", "value"))
def render_ancova_results(ancovaType):
    if ancovaType is not None:
        if ancovaType == "one-way-ancova":
            return html.Div(id="one-way-ancova-results")
        elif ancovaType == "two-way-ancova":
            return html.Div(id="two-way-ancova-results")
    else:
        return {}

@app.callback(Output("one-way-ancova-results", "children"), 
              Input("results-data-upload", "children"),
              Input("ancova-oneway-indep-1", "value"), Input("ancova-oneway-covariate-1", "value"),
              Input("ancova-oneway-dep-1", "value"))
def update_one_way_ancova_results(jsonified_df, ancovaOneWayIndep1, ancovaOneWayCovariate1, ancovaOneWayDep1):
    return {}

@app.callback(Output("two-way-ancova-results","children"),
              Input("results-data-upload", "children"),
              Input("ancova-twoway-indep-1", "value"), Input("ancova-twoway-indep-2", "value"),
              Input("ancova-twoway-covariate-1", "value"), Input("ancova-twoway-dep-1", "value"))
def update_two_way_ancova_results(jsonified_df, ancovaTwoWayIndep1, ancovaTwoWayIndep2, ancovaTwoWayCovariate1, ancovaTwoWayDep1):
    return {}

