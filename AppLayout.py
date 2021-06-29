import dash_core_components as dcc
import dash_html_components as html

def make_layout():
    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.H6(['Upload Data (CSV File): Drag and Drop or ',html.A('Select Files')]),
            multiple=False,
            style={"margin-right" : "10%", "margin-left":"10%", "borderWidth":"1px", "borderRadius":"5px",
            "textAlign":"center", "borderStyle":"dashed","height":"60px", "lineHeight":"60px"}
        ),
        html.Div(id='results-data-upload', style={'display' : 'none'}),
        html.Div(id="variable-list", style={"display": "none"}),

        html.Div([
            html.Button("Generate Report", id="generate-report"), 
            dcc.Download(id="download-report")
            ], style={"textAlign":"center"}),

        dcc.Dropdown(id='independent-var-dropdown', placeholder="Select independent variables", multi=True),        
        html.Div(id="independent-var-list", style={"display": "none"}),

        dcc.Dropdown(id='dependent-var-dropdown', placeholder="Select dependent variables", multi=True),
        html.Div(id="dependent-var-list", style={"display": "none"}),

        html.Div([
            dcc.Tabs(id="tabs-selection", value="dist-analysis", children=[
                dcc.Tab(label = "Distribution Analysis", id="dist-analysis", value="dist-analysis"),
                dcc.Tab(label = "Correlation Analysis", id="corr-analysis", value="corr-analysis"),
                dcc.Tab(label = "Factor Analysis / Extraction", id="fact-analysis-extraction", value="fact-analysis-extraction"),
                dcc.Tab(label = "Design of Experiments", id="doe", value="doe")
        ]),
        html.Div(id="tabs-content")
        ])
    ])