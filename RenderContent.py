from DashApp import app
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


@app.callback(Output("tabs-content", "children"), Input("tabs-selection", "value"))
def render_tabs_content(tab):
    if tab=="dist-analysis":
        return html.Div([
            dcc.Tabs(id="dist-selection", value="scatter-plot", children=[
                dcc.Tab(label="Scatter Plot Matrix", value="scatter-plot"),
                dcc.Tab(label="Distribution Plot", value="distribution-plot"),
                dcc.Tab(label="Box Plot", value="box-plot")
            ]),
            html.Div(id="dist-tabs-content")
            ])
    elif tab=="corr-analysis":
        return html.Div([
            dcc.Tabs(id="corr-selection", value="parallel-coord", children=[
                dcc.Tab(label="Parallel Coordinates", value="parallel-coord"),
                dcc.Tab(label="Correlation Heat Map", value="correlation-heat-map"),
                dcc.Tab(label="2D Plot", value="2d-plot"),
                dcc.Tab(label="3D Plot", value="3d-plot")
            ]),
            html.Div(id="corr-tabs-content")
        ])
    elif tab=="fact-analysis-extraction":
        return html.Div([
            dcc.Tabs(id="fact-selection", value="pca-analysis", children=[
                dcc.Tab(label="Principal Component Analysis", value="pca-analysis"),
                dcc.Tab(label="Exploratory Factor Analysis", value="efa-analysis")
            ]),
            html.Div(id="fact-tabs-content")
        ])
    elif tab=="doe":
        return html.Div([
            dcc.Tabs(id="doe-selection", value="sobol-analysis", children=[
                dcc.Tab(label="SOBOL Sensitivity Indices", value="sobol-analysis"),
                dcc.Tab(label="Delta Sensitivity Indices", value="delta-analysis"),
                dcc.Tab(label="ANOVA", value="anova"),
                dcc.Tab(label="ANCOVA", value="ancova"),
                dcc.Tab(label="MANOVA", value="manova"),
                dcc.Tab(label="MANCOVA", value="mancova")
            ]),
            html.Div(id="doe-tabs-content")
        ])

@app.callback(Output("dist-tabs-content", "children"), Input("dist-selection", "value"))
def render_dist_tab_content(subtab):
    if subtab=="scatter-plot":
        return html.Div(children=[
            html.H3(children="Scatter Plot Matrix", style={"textAlign": "center"}),
            html.P("Color by category"),
            dcc.Dropdown(id="scatter-plot-matrix-color", placeholder="Select categorical variable for color", multi=False),
            dcc.Graph(id="Scatter-plot-matrix", style={"height": "60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="distribution-plot":
        return html.Div(children=[
            html.H3(children="Distribution Plot", style={"textAlign": "center"}),
            dcc.Graph(id="Distribution-plot", style={"height":"60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="box-plot":
        return html.Div(children=[
            html.H3(children="Box Plot", style={"textAlign": "center"}),
            dcc.Graph(id="Box-plot", style={"height":"60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})


@app.callback(Output("corr-tabs-content", "children"), Input("corr-selection","value"))
def render_corr_tab_content(subtab):
    if subtab=="parallel-coord":
        return html.Div(children=[
            html.H3(children="Parallel Coordinates Plot", style={"textAlign": "center"}),
            html.P("Color scale"),
            dcc.Dropdown(id="parallel-colorscale", placeholder="Select variable for color scale", multi=False),
            dcc.Graph(id="Parallel-axis-diagram", style={"height": "60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="correlation-heat-map":
        return html.Div(children=[
            html.H3(children="Correlation Heat Map", style={"textAlign": "center"}),
            dcc.Graph(id="Correlation-heatmap", style={"height" :"60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="2d-plot":
        models={"Linear Regression", "Decision Tree", "k-NN"}
        return html.Div(children=[
            html.H3(children="2D Plot", style={"textAlign": "center"}),
            html.P("Axes variables"),
            dcc.Dropdown(id="2d-x-axis-var", placeholder="Select x axis variable", multi=False),
            dcc.Dropdown(id="2d-y-axis-var", placeholder="Select y axis variable", multi=False),
            html.P("Color scale"),
            dcc.Dropdown(id="2d-graph-color-scale", placeholder="Select variable for color scale", multi=False),
            html.P("Select regression model"),
            dcc.Dropdown(id="2d-regression-models", placeholder="Select regression model", options= [{"label": i, "value": i} for i in models] , multi=False),
            dcc.Graph(id="2d-graph", style={"height":"60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="3d-plot":
        return html.Div(children=[
            html.H3(children="3D Plot", style={"textAlign": "center"}),
            html.P("Axes variables"),
            dcc.Dropdown(id="3d-x-axis-var", placeholder="Select x axis variable", multi=False),
            dcc.Dropdown(id="3d-y-axis-var", placeholder="Select y axis variable", multi=False),
            dcc.Dropdown(id="3d-z-axis-var", placeholder="Select z axis variable", multi=False),
            html.P("Color scale"),
            dcc.Dropdown(id="3d-graph-color-scale", placeholder="Select variable for color scale", multi=False),
            dcc.Graph(id="3d-graph", style={"height":"60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})


@app.callback(Output("fact-tabs-content", "children"), Input("fact-selection", "value"))
def render_fact_tabs_content(subtab):
    if subtab=="pca-analysis":
        return html.Div(children=[
            html.H3(children="Principal Component Analysis", style={"textAlign": "center"}),
            html.P("Number of components"),
            dcc.Slider(id="pca-slider", min=2, max=5, value=3, marks={i: str(i) for i in range(2,6)}),
            html.P("Color scale"),
            dcc.Dropdown(id="pca-colorscale", placeholder="Select variable for color scale", multi=False),
            dcc.Graph(id="PCA-plot", style={"height" : "60vh"}),
            html.H4("PCA Loadings", style={"textAlign": "center"}),
            dcc.Graph(id="PCA-Loadings-plot", style={"height":"60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="efa-analysis":
        return html.Div(children=[
            html.H3(children="Exploratory Factory Analysis", style={"textAlign":"center"}),
            dcc.Graph(id="efa-scree-plot", style={"height": "60vh"}),
            html.H5("Select number of factors"),
            dcc.Slider(id="efa-slider", min=1, max=20, value=2, marks={i:str(i) for i in range(1,20)}),
            html.H4(children="Factor Loadings", style={"textAlign":"center"}),
            dcc.Graph(id="fa-loading-radar-chart", style={"height": "60vh"}),
            html.H4(children="Factor Loading Matrix", style={"textAlign": "center"}),
            html.Div(id="fa-loading-table")
        ], style={"margin-right": "10%", "margin-left":"10%"})


@app.callback(Output("doe-tabs-content", "children"), Input("doe-selection", "value"))
def render_doe_tab_content(subtab):
    if subtab=="sobol-analysis":
        return html.Div(children=[
            html.H3(children="SOBOL Analysis Results", style={"textAlign": "center"}),
            dcc.Graph(id="SOBOL-analysis-results", style= {"height": "60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="delta-analysis":
        return html.Div(children=[
            html.H3(children="Delta Analysis Results", style={"textAlign": "center"}),
            dcc.Graph(id="Delta-analysis-results", style={"height": "60vh"})
            ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="anova":
        return html.Div(children=[
            html.H3(children="ANOVA", style={"textAlign": "center"}),
            dcc.Dropdown(id="anova-type-dropdown", options=[
                {"label":"One-way ANOVA", "value":"one-way-anova"},
                {"label":"Two-way ANOVA", "value":"two-way-anova"}
            ], value="one-way-anova"),
            html.Div(id="anova-view"),
            html.Div(id="anova-results")
        ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="ancova":
        return html.Div(children=[
            html.H3(children="ANCOVA", style={"textAlign": "center"}),
            dcc.Dropdown(id="ancova-type-dropdown", options=[
                {"label":"One-way ANCOVA", "value":"one-way-ancova"},
                {"label":"Two-way ANCOVA", "value":"two-way-ancova"}
            ], value="one-way-ancova"),
            html.Div(id="ancova-view"),
            html.Div(id="ancova-results")
        ], style={"margin-right":"10%", "margin-left": "10%"})
    elif subtab=="manova":
        return html.Div(children=[
            html.H3(children="MANOVA", style={"textAlign":"center"}),
            dcc.Dropdown(id="manova-type-dropdown", options=[
                {"label": "One-way MANOVA", "value": "one-way-manova"},
                {"label": "Two-way MANOVA", "value": "two-way-manova"}
            ], value="one-way-manova"),
            html.Div(id="manova-view"),
            html.Div(id="manova-results")
        ], style={"margin-right": "10%", "margin-left": "10%"})
    elif subtab=="mancova":
        return html.Div(children=[
            html.H3(children="MANCOVA", style={"textAlign": "center"}),
            dcc.Dropdown(id="mancova-type-dropdown", options=[
                {"label": "One-way MANCOVA", "value": "one-way-mancova"},
                {"label": "Two-way MANCOVA", "value": "two-way-mancova"}
            ], value="one-way-mancova"),
            html.Div(id="mancova-view"),
            html.Div(id="mancova-results")
        ], style={"margin-right": "10%", "margin-left": "10%"})





