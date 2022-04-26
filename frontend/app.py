# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from os import path
from devtools import debug
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from specklepy.api.credentials import StreamWrapper
from data_plots import get_commit_embed_str
from data_plots import create_plots, get_stream_wrapper

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Roboto:wght@400;700&display=swap"
        "family=Space+Mono:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "carbon reports"


app.layout = html.Div(
    [
        # represents the URL bar, doesn't render anything
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                html.H1(
                    children="automated workflows with specklepy",
                    className="header-title",
                ),
                html.P(
                    children="""
                    Speckle is the open source data platform for AEC.
                    We free your data from proprietary file formats so you can own
                    and access your data wherever you need it - including Python!
                    """,
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Iframe(id="viewer", className="Container", style={"width": "80%", "height": "550px", "display": "block", "margin": "auto", "margin-top": "50px"}),
        html.Div(
            id="page-content",
            className="container",
        ),
    ],
)

@app.callback(
    dash.dependencies.Output("viewer", "src"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_viewer(pathname):
    try:
        return get_commit_embed_str(pathname)
    except Exception:
        return None

@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    """Dynamically switch out the `page-content` div based on the URL path"""

    if not pathname.startswith("/streams"):
        return html.Div(
            [
                html.H3(
                    "Invalid url. Please make sure you've followed a valid report url."
                ),
                html.Div(
                    [
                        "The url path should be in the form '/streams/STREAM-ID/commits/COMMIT-ID'"
                    ]
                ),
            ]
        )
    plots = create_plots(pathname)

    if not plots:
        return html.Div(
            [
                html.H3("Error receiving carbon data."),
                html.Div(
                    [
                        "Ensure you have followed the correct link and that you have permission to receive from this stream."
                    ]
                ),
            ]
        )

    return html.Div(
        [
            html.Div(
                children=[dcc.Graph(id=name, figure=plot)],
                className="card",
            )
            for name, plot in plots.items()
        ],
        className="container",
    )


if __name__ == "__main__":
    app.run_server()
