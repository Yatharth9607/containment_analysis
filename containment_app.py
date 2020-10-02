# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:13:55 2019

@author: SESA539950
"""

import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import base64
import containment_solver

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    "background": "#ffffff",
    "text": "darkgrey",
    "dark grey": "#626469",
    "anthracite grey": "3333333",
}

image_filename = "schneider_LIO_White_RGB.png"
encoded_header_image = base64.b64encode(open(image_filename, "rb").read())
life_green = "#3DCD58"


def title_header():
    return html.Div(
        children=[
            html.Img(
                src="data:image/png;base64,{}".format(encoded_header_image.decode()),
                style={"width": 200, "height": 55.1428571429},
            ),
            html.Div(
                style={"flexGrow": 10},
                children=[
                    html.H1(
                        children="Containment Analysis Tool",
                        style={
                            "textAlign": "left",
                            "color": "white",
                            "margin": 0,
                            "padding-left": "25%",
                        },
                    )
                ],
            ),
        ],
        style={
            "display": "flex",
            "backgroundColor": life_green,
            "padding": "1rem 0.5rem 1rem 0.5rem",
            "marginBottom": "2rem",
        },
    )


data_center = {
    "Dropped ceiling (with flooded supply)": [
        "Hot-aisle (Ducted)",
        "Ducted Rack",
        "None",
    ],
    "Raised-floor": ["Cold-aisle", "None", "External supply, Cold-aisle"],
    "Raised-floor with dropped ceiling": ["Hot-aisle (Ducted)", "Cold-aisle", "None"],
    "Close-coupled Cooling": ["Hot-aisle", "Cold-aisle"],
}

option = [
    p + ", " + q
    for p in data_center.keys()
    for q in list(data_center.values())[list(data_center.keys()).index(p)]
]

encoded_image = [base64.b64encode(open(i + ".PNG", "rb").read()) for i in option]

unit_options = ["SI", "US"]

app.layout = html.Div(
    children=[
        # TITLE
        title_header(),
        # CONTAINMENT TYPE
        html.Div(
            className="row",
            children=[
                html.Div(
                    style={"style": "flex", "flex-direction": "column"},
                    children=[
                        html.H4(
                            children="Data Center Architecture",
                            style={
                                "textAlign": "left",
                                "color": "grey",
                                "borderBottom": "solid 1px grey",
                            },
                        ),
                        html.H6(children="Type of Air Distribution:"),
                        dcc.RadioItems(
                            id="architecture",
                            style={"borderBottom": "dotted 1px grey"},
                            options=[
                                {"label": k, "value": k} for k in data_center.keys()
                            ],
                            value=list(data_center.keys())[0],
                        ),
                        html.H6(children="Containment Type:"),
                        dcc.RadioItems(
                            id="containment",
                            style={"borderBottom": "dotted 1px grey"},
                            options=[
                                {"label": k, "value": k}
                                for k in list(data_center.values())[0]
                            ],
                            value=list(data_center.values())[0][0],
                        ),
                        # SCHEMATIC DIAGRAM
                        html.H4(
                            children="Schematic Diagram",
                            style={
                                "textAlign": "left",
                                "color": "grey",
                                "borderBottom": "solid 1px grey",
                            },
                        ),
                        html.Img(
                            id="schematic-id",
                            style={"display": "flex", "width": "300px"},
                        ),
                        html.H6(id="schematic_type-id", style={"textAlign": "center"}),
                    ],
                    className="three columns",
                ),
                # DATA CENTER CONFIGURATION
                html.Div(
                    style={"style": "flex", "flex-direction": "column"},
                    children=[
                        html.H4(
                            children="Data Center Configuration",
                            style={
                                "textAlign": "left",
                                "color": "grey",
                                "borderBottom": "solid 1px grey",
                            },
                        ),
                        html.Div(style={"margin-bottom": "4%"}),
                        html.Div(
                            id="whitespace_area",
                            children=[
                                html.Label(
                                    children="Whitespace Area (ft\u00B2)",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Input(
                                    id="w_area-id",
                                    value=100,
                                    type="number",
                                    min=1,
                                    max=100000,
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="cooling_unit_area",
                            children=[
                                html.Label(
                                    children="Cooling Unit (Obstructed Whitespace) Area (ft\u00B2)",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Input(
                                    id="obs_area-id",
                                    value=0,
                                    type="number",
                                    min=0,
                                    max=100000,
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            children=[
                                html.Label(
                                    children="Cooling Airflow (cfm)",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Input(
                                    id="Q_cool-id",
                                    value=5000,
                                    type="number",
                                    min=0,
                                    max=10000,
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="external_supply_Q_c",
                            children=[
                                html.Label(
                                    children="External: Q_c (cfm)",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                        "width": "250px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="Q_c_type-id",
                                    value=1,
                                    options=[
                                        {"label": "supply", "value": 1},
                                        {"label": "return", "value": -1},
                                    ],
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                        "display": "inline-block",
                                    },
                                ),
                                dcc.Input(
                                    id="Q_c-id",
                                    value=500,
                                    type="number",
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="external_supply_Q_room",
                            children=[
                                html.Label(
                                    children="External: Q_room (cfm)",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                        "width": "250px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="Q_room_type-id",
                                    value=-1,
                                    options=[
                                        {"label": "supply", "value": 1},
                                        {"label": "return", "value": -1},
                                    ],
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                        "display": "inline-block",
                                    },
                                ),
                                dcc.Input(
                                    id="Q_room-id",
                                    value=1000,
                                    type="number",
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="external_supply_Q_FP",
                            children=[
                                html.Label(
                                    children="External: Q_FP (cfm)",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                        "width": "250px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="Q_FP_type-id",
                                    value=1,
                                    options=[
                                        {"label": "supply", "value": 1},
                                        {"label": "return", "value": -1},
                                    ],
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                        "display": "inline-block",
                                    },
                                ),
                                dcc.Input(
                                    id="Q_FP-id",
                                    value=500,
                                    type="number",
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="avg_q",
                            children=[
                                html.Label(
                                    children="Avg IT Power per Rack (kW)",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Input(
                                    id="q_IT-id",
                                    value=5,
                                    type="number",
                                    min=0,
                                    max=100,
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            children=[
                                html.Label(
                                    children="Number of Racks",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Input(
                                    id="n_rack-id",
                                    value=5,
                                    type="number",
                                    min=1,
                                    max=100,
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="number_tile_dc",
                            children=[
                                html.Label(
                                    children="Number of Perforated Ceiling Tiles",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Input(
                                    id="n_tile-id",
                                    value=5,
                                    type="number",
                                    min=1,
                                    max=100,
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="dc_perforated_tile",
                            children=[
                                html.Label(
                                    children="Perforated Ceiling Tile Type (% open area)",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="dc_b_tile-id",
                                    options=[
                                        {"label": "25", "value": 0.25},
                                        {"label": "40", "value": 0.40},
                                        {"label": "56", "value": 0.56},
                                        {"label": "80", "value": 0.80},
                                    ],
                                    value=0.40,
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                        "display": "inline-block",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="dc_construction",
                            children=[
                                html.Label(
                                    children="Dropped Ceiling Construction",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="f_DC-id",
                                    options=[
                                        {"label": "Well Sealed", "value": 200000},
                                        {"label": "Typical", "value": 100000},
                                        {"label": "Leaky", "value": 8000},
                                    ],
                                    value=100000,
                                    style={
                                        "margin-right": "10px",
                                        "width": "125px",
                                        "text-align": "center",
                                        "display": "inline-block",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="rf_perforated_tile",
                            children=[
                                html.Label(
                                    children="Perforated Floor Tile Type (% open area)",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="rf_b_tile-id",
                                    options=[
                                        {"label": "25", "value": 0.25},
                                        {"label": "40", "value": 0.40},
                                        {"label": "56", "value": 0.56},
                                    ],
                                    value=0.40,
                                    style={
                                        "margin-right": "10px",
                                        "width": "85px",
                                        "text-align": "center",
                                        "display": "inline-block",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="rf_construction",
                            children=[
                                html.Label(
                                    children="Raised-floor Construction",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="f_floor-id",
                                    options=[
                                        {"label": "Well Sealed", "value": 72845000},
                                        {"label": "Typical", "value": 181900},
                                        {"label": "Leaky", "value": 116400},
                                    ],
                                    value=181900,
                                    style={
                                        "margin-right": "10px",
                                        "width": "125px",
                                        "text-align": "center",
                                        "display": "inline-block",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        html.Div(
                            id="cable_cutouts",
                            children=[
                                html.Label(
                                    children="Raised-floor Cable Cutouts",
                                    style={
                                        "padding-left": "10px",
                                        "padding-right": "10px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="cut_area-id",
                                    options=[
                                        {"label": "None", "value": 0.000000001},
                                        {"label": "Minimal", "value": 0.00348},
                                        {"label": "Typical", "value": 0.03484},
                                        {"label": "Large", "value": 0.04645},
                                    ],
                                    value=0.00348,
                                    style={
                                        "margin-right": "10px",
                                        "width": "125px",
                                        "text-align": "center",
                                        "display": "inline-block",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "padding-right": "20px",
                            },
                        ),
                        # ADVANCED OPTIONS
                        html.Br(),
                        html.Div(
                            id="modal_f",
                            children="Invalid input - Net Floor Area = 0 and calculated Floor Tile Resistance = Inf",
                        ),
                        html.Div(
                            id="modal_c",
                            children="Invalid input - Net Ceiling Area = 0 and calculated Ceiling Tile Resistance = Inf",
                        ),
                        html.Br(),
                        html.Div(
                            children=[
                                html.Button(
                                    children="Advanced",
                                    id="button",
                                    n_clicks=0,
                                    style={
                                        "display": "flex",
                                        "justify-content": "center",
                                        "width": "120px",
                                        "border-radius": "50%",
                                    },
                                )
                            ],
                            style={"display": "flex", "justify-content": "center"},
                        ),
                        html.Br(),
                        html.Div(
                            id="advanced_options-id",
                            children=[
                                html.Label(
                                    "Per Rack Leakage Resistances (Pa/(m\u00B3/s)\u00B2):"
                                ),
                                html.Br(),
                                html.Div(
                                    id="a_SP_display-id",
                                    children=[
                                        html.Label(
                                            children="Server Plane Leakage Resistance",
                                            style={
                                                "padding-left": "10px",
                                                "padding-right": "10px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="a_SP-id",
                                            value=1530,
                                            type="number",
                                            min=0,
                                            max=100000,
                                            style={
                                                "margin-right": "10px",
                                                "width": "75px",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-right": "20px",
                                    },
                                ),
                                html.Div(
                                    id="a_RL_display-id",
                                    children=[
                                        html.Label(
                                            children="Rear-to-Top Leakage Resistance",
                                            style={
                                                "padding-left": "10px",
                                                "padding-right": "10px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="a_RL-id",
                                            value=192,
                                            type="number",
                                            min=0,
                                            max=100000,
                                            style={
                                                "margin-right": "10px",
                                                "width": "75px",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-right": "20px",
                                    },
                                ),
                                html.Div(
                                    id="a_D_HACS_display-id",
                                    children=[
                                        html.Label(
                                            children="Ducted HACS Duct Resistance",
                                            style={
                                                "padding-left": "10px",
                                                "padding-right": "10px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="a_D_HACS-id",
                                            value=8.8,
                                            type="number",
                                            min=0,
                                            max=100000,
                                            style={
                                                "margin-right": "10px",
                                                "width": "75px",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-right": "20px",
                                    },
                                ),
                                html.Div(
                                    id="a_D_rack_display-id",
                                    children=[
                                        html.Label(
                                            children="Ducted Rack Duct Resistance",
                                            style={
                                                "padding-left": "10px",
                                                "padding-right": "10px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="a_D_rack-id",
                                            value=34,
                                            type="number",
                                            min=0,
                                            max=100000,
                                            style={
                                                "margin-right": "10px",
                                                "width": "75px",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-right": "20px",
                                    },
                                ),
                                html.Br(),
                                html.Div(
                                    id="rho_display-id",
                                    children=[
                                        html.Label(
                                            children="Density of Air (kg/m\u00B3)",
                                            style={
                                                "padding-left": "10px",
                                                "padding-right": "10px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="rho-id",
                                            value=1.19,
                                            type="number",
                                            min=0,
                                            max=100,
                                            style={
                                                "margin-right": "10px",
                                                "width": "75px",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-right": "20px",
                                    },
                                ),
                                html.Div(
                                    id="q_IT_rack_display-id",
                                    children=[
                                        html.Label(
                                            children="IT Airflow per Avg Rack Power (cfm/kW)",
                                            style={
                                                "padding-left": "10px",
                                                "padding-right": "10px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="q_IT_rack-id",
                                            value=125,
                                            type="number",
                                            min=0,
                                            max=1000,
                                            style={
                                                "margin-right": "10px",
                                                "width": "75px",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-right": "20px",
                                    },
                                ),
                            ],
                        ),
                    ],
                    className="four columns",
                ),
                # INTERMEDIATE CALCULATIONS
                html.Div(
                    className="five columns",
                    style={"display": "flex", "flex-direction": "column"},
                    children=[
                        html.Div(
                            className="twelve columns",
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "padding-left": "10px",
                                "padding-right": "10px",
                            },
                            children=[
                                html.Div(
                                    children=[
                                        html.H4(
                                            children="Intermediate Calculations",
                                            style={
                                                "display": "inline-block",
                                                "textAlign": "left",
                                                "color": "grey",
                                            },
                                        ),
                                        html.Div(
                                            children=[
                                                html.Label(
                                                    children="Units: ",
                                                    style={
                                                        "style": "flex",
                                                        "font-size": "18px",
                                                        "padding-left": "30%",
                                                        "margin-top": "1%",
                                                    },
                                                ),
                                                dcc.Dropdown(
                                                    id="unit",
                                                    style={
                                                        "display": "inline-block",
                                                        "width": "50px",
                                                        "textAlign": "center",
                                                        "padding-left": "5%",
                                                    },
                                                    options=[
                                                        {"label": k, "value": k}
                                                        for k in unit_options
                                                    ],
                                                    value=unit_options[1],
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "textAlign": "left",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "textAlign": "left",
                                        "borderBottom": "solid 1px grey",
                                    },
                                ),
                                html.Br(style={"line-height": "1%"}),
                                html.Div(
                                    id="g_air_ratio",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Global Air Ratio",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="global_air_ratio-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            children="-",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="net_f_area",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Net Floor Area",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="net_f_area-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="net_f_area_unit",
                                            children="m\u00B2",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="net_c_area",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Net Ceiling Area",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="net_c_area-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="net_c_area_unit",
                                            children="m\u00B2",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Label(
                                    children="Resistances:-",
                                    style={
                                        "font-weight": "bold",
                                        "padding-bottom": "8px",
                                    },
                                ),
                                html.Div(
                                    id="sp_res",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Total Server Plane Resistance (\u03B1_SP)",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="alpha_sp-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="sp_res_unit",
                                            children="Pa/(m\u00B3/s)\u00B2",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="rl_res",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Total Rack Leakage Resistance (\u03B1_RL)",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="alpha_rl-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="rl_res_unit",
                                            children="Pa/(m\u00B3/s)\u00B2",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="rf_tile_res",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Raised-floor Tile Resistance (\u03B1_FT)",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="rf_alpha_T-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="rf_tile_res_unit",
                                            children="Pa/(m\u00B3/s)\u00B2",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="dc_tile_res",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Dropped Ceiling Tile Resistance (\u03B1_CT)",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="dc_alpha_T-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="dc_tile_res_unit",
                                            children="Pa/(m\u00B3/s)\u00B2",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="duct_res",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Duct Resistance (\u03B1_D)",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="alpha_D-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="duct_res_unit",
                                            children="Pa/(m\u00B3/s)\u00B2",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="rf_leakage_res",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Raised-floor Leakage Resistance (\u03B1_RF)",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="alpha_RF-id",
                                            # children='-',
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="rf_leakage_res_unit",
                                            children="Pa/(m\u00B3/s)\u00B2",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="dc_leakage_res",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Dropped Ceiling Leakage Resistance (\u03B1_DC)",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="alpha_DC-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="dc_leakage_res_unit",
                                            children="Pa/(m\u00B3/s)\u00B2",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                # PRESSURE
                                html.H4(
                                    children="Pressure",
                                    style={
                                        "display": "flex",
                                        "textAlign": "left",
                                        "color": "grey",
                                        "borderBottom": "solid 1px grey",
                                    },
                                ),
                                html.Div(
                                    id="rf_plenum_pressure",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Raised-floor Plenum Pressure",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="RF_plenum_p-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="rf_plenum_p_unit",
                                            children="Pa",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="dc_plenum_pressure",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Dropped Ceiling Plenum Pressure",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="DC_plenum_p-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="dc_plenum_p_unit",
                                            children="Pa",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="containment_pressure",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Containment Pressure",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="containment_p-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="containment_p_unit",
                                            children="Pa",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                # AIRFLOW
                                html.H4(
                                    children="Airflow",
                                    style={
                                        "display": "flex",
                                        "textAlign": "left",
                                        "color": "grey",
                                        "borderBottom": "solid 1px grey",
                                    },
                                ),
                                html.Div(
                                    id="Q_IT",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Total IT Airflow",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="Q_IT-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="Q_IT_unit",
                                            children="m\u00B3/s",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Total Cooling Airflow",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="Q_AC-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="Q_AC_unit",
                                            children="m\u00B3/s",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="Q_SP",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Server Plane Leakage Airflow",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="Q_SP-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="Q_SP_unit",
                                            children="m\u00B3/s",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="Q_RL",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Rack Leakage Airflow",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="Q_RL-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="Q_RL_unit",
                                            children="m\u00B3/s",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="duct_airflow",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Duct Airflow",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="Q_D-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="Q_D_unit",
                                            children="m\u00B3/s",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="rf_tile_airflow",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Raised-floor Tile Airflow",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="rf_Q_T-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="rf_Q_T_unit",
                                            children="m\u00B3/s",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="dc_tile_airflow",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Dropped Ceiling Tile Airflow",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="dc_Q_T-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="dc_Q_T_unit",
                                            children="m\u00B3/s",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="dc_leakage",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Dropped Ceiling Leakage",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="Q_DC-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="Q_DC_unit",
                                            children="m\u00B3/s",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="rf_leakage",
                                    style={
                                        "display": "flex",
                                        "justify-content": "space-between",
                                        "padding-bottom": "8px",
                                    },
                                    children=[
                                        html.Div(
                                            children="Raised-floor Leakage",
                                            className="eight columns",
                                        ),
                                        html.Div(
                                            id="Q_RF-id",
                                            children="-",
                                            style={
                                                "color": "green",
                                                "font-weight": "bold",
                                                "textAlign": "right",
                                            },
                                            className="two columns",
                                        ),
                                        html.Div(
                                            id="Q_RF_unit",
                                            children="m\u00B3/s",
                                            style={
                                                "color": "grey",
                                                "textAlign": "left",
                                            },
                                            className="two columns",
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
            ],
        ),
    ]
)


# CASE OPTIONS


@app.callback(Output("containment", "options"), [Input("architecture", "value")])
def set_cases_options(selected_simulation):
    return [{"label": i, "value": i} for i in data_center[selected_simulation]]


@app.callback(Output("containment", "value"), [Input("containment", "options")])
def set_cases_value(available_options):
    return available_options[0]["value"]


# DYNAMIC DISPLAY


@app.callback(
    [
        Output("whitespace_area", "style"),
        Output("cooling_unit_area", "style"),
        Output("net_f_area", "style"),
    ],
    [Input("architecture", "value")],
)
def group_1(architecture):
    if architecture == "Close-coupled Cooling":
        return [{"display": "none"}, {"display": "none"}, {"display": "none"}]
    else:
        return [
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
        ]


@app.callback(
    [
        Output("rf_perforated_tile", "style"),
        Output("rf_construction", "style"),
        Output("cable_cutouts", "style"),
        Output("rf_tile_res", "style"),
        Output("rf_leakage_res", "style"),
        Output("rf_plenum_pressure", "style"),
        Output("rf_tile_airflow", "style"),
        Output("rf_leakage", "style"),
    ],
    [Input("architecture", "value")],
)
def group_2(architecture):
    if (
        architecture == "Raised-floor"
        or architecture == "Raised-floor with dropped ceiling"
    ):
        return [
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
        ]
    else:
        return [
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        ]


@app.callback(
    [
        Output("number_tile_dc", "style"),
        Output("dc_perforated_tile", "style"),
        Output("dc_tile_res", "style"),
        Output("dc_tile_airflow", "style"),
    ],
    [Input("architecture", "value"), Input("containment", "value")],
)
def group_3(architecture, containment):
    if (
        architecture == "Dropped ceiling (with flooded supply)"
        or architecture == "Raised-floor with dropped ceiling"
    ):
        if containment == "Cold-aisle" or containment == "None":
            return [
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-right": "20px",
                },
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-right": "20px",
                },
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-bottom": "8px",
                },
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-bottom": "8px",
                },
            ]
        else:
            return [
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            ]
    else:
        return [
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        ]


@app.callback(
    [
        Output("a_D_HACS_display-id", "style"),
        Output("a_D_rack_display-id", "style"),
        Output("duct_res", "style"),
        Output("duct_airflow", "style"),
    ],
    [Input("architecture", "value"), Input("containment", "value")],
)
def group_4(architecture, containment):
    if (
        architecture == "Dropped ceiling (with flooded supply)"
        or architecture == "Raised-floor with dropped ceiling"
    ):
        if containment == "Hot-aisle (Ducted)":
            return [
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-right": "20px",
                },
                {"display": "none"},
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-bottom": "8px",
                },
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-bottom": "8px",
                },
            ]
        elif containment == "Ducted Rack":
            return [
                {"display": "none"},
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-right": "20px",
                },
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-bottom": "8px",
                },
                {
                    "display": "flex",
                    "justify-content": "space-between",
                    "padding-bottom": "8px",
                },
            ]
        else:
            return [
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            ]
    else:
        return [
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        ]


@app.callback(
    [
        Output("dc_construction", "style"),
        Output("dc_leakage_res", "style"),
        Output("dc_plenum_pressure", "style"),
        Output("dc_leakage", "style"),
        Output("net_c_area", "style"),
    ],
    [Input("architecture", "value")],
)
def group_5(architecture):
    if (
        architecture == "Dropped ceiling (with flooded supply)"
        or architecture == "Raised-floor with dropped ceiling"
    ):
        return [
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
        ]
    else:
        return [
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        ]


@app.callback(
    [
        Output("avg_q", "style"),
        Output("g_air_ratio", "style"),
        Output("sp_res", "style"),
        Output("Q_IT", "style"),
        Output("Q_SP", "style"),
        Output("Q_RL", "style"),
        Output("containment_pressure", "style"),
    ],
    [Input("containment", "value")],
)
def group_6(containment):
    if containment == "None":
        return [
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        ]
    else:
        return [
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            },
        ]


@app.callback([Output("rl_res", "style")], [Input("containment", "value")])
def group_7(containment):
    if (
        containment == "Cold-aisle"
        or containment == "None"
        or containment == "External supply, Cold-aisle"
    ):
        return [{"display": "none"}]
    else:
        return [
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-bottom": "8px",
            }
        ]


@app.callback(
    [Output("n_rack-id", "value"), Output("n_rack-id", "readOnly")],
    [Input("containment", "value")],
)
def group_8(containment):
    if containment == "Ducted Rack":
        return [1, True]
    else:
        return [5, False]


@app.callback(
    [
        Output("external_supply_Q_c", "style"),
        Output("external_supply_Q_room", "style"),
        Output("external_supply_Q_FP", "style"),
    ],
    [Input("containment", "value")],
)
def group_9(containment):
    if containment == "External supply, Cold-aisle":
        return [
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
            {
                "display": "flex",
                "justify-content": "space-between",
                "padding-right": "20px",
            },
        ]
    else:
        return [{"display": "none"}, {"display": "none"}, {"display": "none"}]


# CALCULATIONS

# AIRFLOW CALCULATIONS
@app.callback(
    [
        Output("containment_p-id", "children"),
        Output("RF_plenum_p-id", "children"),
        Output("DC_plenum_p-id", "children"),
        Output("global_air_ratio-id", "children"),
        Output("net_f_area-id", "children"),
        Output("net_c_area-id", "children"),
        Output("Q_IT-id", "children"),
        Output("Q_AC-id", "children"),
        Output("Q_SP-id", "children"),
        Output("Q_RL-id", "children"),
        Output("Q_D-id", "children"),
        Output("rf_Q_T-id", "children"),
        Output("dc_Q_T-id", "children"),
        Output("Q_DC-id", "children"),
        Output("Q_RF-id", "children"),
        Output("alpha_sp-id", "children"),
        Output("alpha_rl-id", "children"),
        Output("rf_alpha_T-id", "children"),
        Output("dc_alpha_T-id", "children"),
        Output("alpha_D-id", "children"),
        Output("alpha_RF-id", "children"),
        Output("alpha_DC-id", "children"),
        Output("schematic-id", "src"),
        Output("schematic_type-id", "children"),
        Output("modal_f", "style"),
        Output("modal_c", "style"),
    ],
    [
        Input("architecture", "value"),
        Input("containment", "value"),
        Input("w_area-id", "value"),
        Input("obs_area-id", "value"),
        Input("Q_cool-id", "value"),
        Input("n_rack-id", "value"),
        Input("q_IT-id", "value"),
        Input("rf_b_tile-id", "value"),
        Input("n_tile-id", "value"),
        Input("dc_b_tile-id", "value"),
        Input("f_floor-id", "value"),
        Input("cut_area-id", "value"),
        Input("f_DC-id", "value"),
        Input("a_SP-id", "value"),
        Input("a_RL-id", "value"),
        Input("a_D_HACS-id", "value"),
        Input("a_D_rack-id", "value"),
        Input("rho-id", "value"),
        Input("q_IT_rack-id", "value"),
        Input("unit", "value"),
        Input("Q_c-id", "value"),
        Input("Q_c_type-id", "value"),
        Input("Q_room-id", "value"),
        Input("Q_room_type-id", "value"),
        Input("Q_FP-id", "value"),
        Input("Q_FP_type-id", "value"),
    ],
)
def update_graph(
    architecture,
    containment,
    w_area,
    obs_area,
    Q_cool,
    n_rack,
    q_IT,
    b_tile_rf,
    n_tile,
    b_tile_dc,
    f_floor,
    cut_area,
    f_DC,
    a_SP,
    a_RL,
    a_D_HACS,
    a_D_rack,
    rho,
    q_IT_rack,
    unit,
    Q_c,
    Q_c_type,
    Q_room,
    Q_room_type,
    Q_FP,
    Q_FP_type,
):
    solveFNM = containment_solver.FNMsolver(
        architecture,
        containment,
        w_area,
        obs_area,
        Q_cool,
        n_rack,
        q_IT,
        b_tile_rf,
        n_tile,
        b_tile_dc,
        f_floor,
        cut_area,
        f_DC,
        a_SP,
        a_RL,
        a_D_HACS,
        a_D_rack,
        rho,
        q_IT_rack,
        Q_c_type * Q_c,
        Q_room_type * Q_room,
        Q_FP_type * Q_FP,
    )
    Q, P = solveFNM.calcAirflow()
    global_ar, net_f_area, net_c_area, Q_IT, a = solveFNM.flowRes()
    Q = np.array(Q)
    P = np.array(P)
    a = np.array(a)
    if unit == "US":
        net_f_area = 10.764 * net_f_area
        net_c_area = 10.764 * net_c_area
        P = 0.004015 * P
        Q = 2118.88 * Q
        a = 8.937 * 10 ** (-10) * a

    Q = Q.tolist()
    P = P.tolist()
    a = a.tolist()

    for i in range(np.size(a)):
        if abs(a[i]) < 0.01 or abs(a[i]) > 1000:
            a[i] = f"{a[i]:.2e}"
        else:
            a[i] = f"{a[i]:.2f}"
    for i in range(np.size(Q)):
        if abs(Q[i]) < 0.01 or abs(Q[i]) > 1000:
            Q[i] = f"{Q[i]:.2e}"
        else:
            Q[i] = f"{Q[i]:.2f}"
    for i in range(np.size(P)):
        if abs(P[i]) < 0.01 or abs(P[i]) > 1000:
            P[i] = f"{P[i]:.2e}"
        else:
            P[i] = f"{P[i]:.2f}"

    case = solveFNM.caseFNM()
    src = "data:image/png;base64,{}".format(encoded_image[case - 1].decode())

    if net_f_area == 0.0:
        modal_f = {"display": "block", "border": "dashed", "textAlign": "center"}
    else:
        modal_f = {"display": "none"}

    if net_c_area == 0.0:
        modal_c = {"display": "block", "border": "dashed", "textAlign": "center"}
    else:
        modal_c = {"display": "none"}
    return [
        P[0],
        P[2],
        P[1],
        f"{global_ar:.2f}",
        f"{net_f_area:.2f}",
        f"{net_c_area:.2f}",
        Q[0],
        Q[1],
        Q[2],
        Q[3],
        Q[4],
        Q[5],
        Q[6],
        Q[7],
        Q[8],
        a[0],
        a[1],
        a[2],
        a[3],
        a[4],
        a[5],
        a[6],
        src,
        architecture + ", " + containment + " containment",
        modal_f,
        modal_c,
    ]


@app.callback(
    [
        Output("net_f_area_unit", "children"),
        Output("net_c_area_unit", "children"),
        Output("sp_res_unit", "children"),
        Output("rl_res_unit", "children"),
        Output("rf_tile_res_unit", "children"),
        Output("dc_tile_res_unit", "children"),
        Output("duct_res_unit", "children"),
        Output("rf_leakage_res_unit", "children"),
        Output("dc_leakage_res_unit", "children"),
        Output("rf_plenum_p_unit", "children"),
        Output("dc_plenum_p_unit", "children"),
        Output("containment_p_unit", "children"),
        Output("Q_IT_unit", "children"),
        Output("Q_AC_unit", "children"),
        Output("Q_SP_unit", "children"),
        Output("Q_RL_unit", "children"),
        Output("Q_D_unit", "children"),
        Output("rf_Q_T_unit", "children"),
        Output("dc_Q_T_unit", "children"),
        Output("Q_DC_unit", "children"),
        Output("Q_RF_unit", "children"),
    ],
    [Input("unit", "value")],
)
def unit_update(unit):
    if unit == "SI":
        return [
            "m\u00B2",
            "m\u00B2",
            "Pa/(m\u00B3/s)\u00B2",
            "Pa/(m\u00B3/s)\u00B2",
            "Pa/(m\u00B3/s)\u00B2",
            "Pa/(m\u00B3/s)\u00B2",
            "Pa/(m\u00B3/s)\u00B2",
            "Pa/(m\u00B3/s)\u00B2",
            "Pa/(m\u00B3/s)\u00B2",
            "Pa",
            "Pa",
            "Pa",
            "m\u00B3/s",
            "m\u00B3/s",
            "m\u00B3/s",
            "m\u00B3/s",
            "m\u00B3/s",
            "m\u00B3/s",
            "m\u00B3/s",
            "m\u00B3/s",
            "m\u00B3/s",
        ]
    else:
        return [
            "ft\u00B2",
            "ft\u00B2",
            "inH\u2082O/(cfm\u00B2)",
            "inH\u2082O/(cfm\u00B2)",
            "inH\u2082O/(cfm\u00B2)",
            "inH\u2082O/(cfm\u00B2)",
            "inH\u2082O/(cfm\u00B2)",
            "inH\u2082O/(cfm\u00B2)",
            "inH\u2082O/(cfm\u00B2)",
            "inH\u2082O",
            "inH\u2082O",
            "inH\u2082O",
            "cfm",
            "cfm",
            "cfm",
            "cfm",
            "cfm",
            "cfm",
            "cfm",
            "cfm",
            "cfm",
        ]


@app.callback([Output("advanced_options-id", "style")], [Input("button", "n_clicks")])
def advanced_option(n_clicks):
    if n_clicks % 2 == 0:
        return [{"display": "none"}]
    else:
        return [
            {
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "space-between",
            }
        ]


if __name__ == "__main__":
    app.run_server(debug=False, port=8060)
