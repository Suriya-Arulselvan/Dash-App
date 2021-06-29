import dash
from AppLayout import make_layout
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.layout = make_layout()

from DataUploadAndVarSelection import *
from RenderContent import *

from Plots.ScatterPlot import *
from Plots.ParallelAxisPlot import *
from Plots.DistributionPlot import *
from Plots.BoxPlot import *
from Plots.CorrelationHeatMap import *
from Plots.SobolAnalysisPlot import *
from Plots.DeltaAnalysisPlot import *
from Plots.PCAPlots import *
from Plots.EFAPlots import *
from Plots.Graph2D import *
from Plots.Graph3D import *
from Plots.AnovaAncova import *
from Plots.ManovaMancova import *


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)