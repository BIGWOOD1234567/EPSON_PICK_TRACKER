import os
import pathlib
from datetime import date
import re

import dash_daq as daq
import dash_table
import pandas as pd
import plotly.express as px

import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "TEST_MOCK_DATA.csv")))


# ========== initialize save data =============


def init_value_setter_store():
    # Initialize store data
    state_dict = {"Rate_Total": "110%",
                  "Date": "NONE",
                  "Department": "NONE",
                  "User": "111",
                  "Type": "NONE", }
    return state_dict


# ========== build tabs function =============
def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("EPSON PICK TRACKER"),
                    html.H6("Productivity Report"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.Img(id="logo", src=app.get_asset_url("epson-logo.png")),
                ],
            ),
        ],
    )


# ========= build tabs function ===========

def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Filter Settings",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Pick Chart Dashboard",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


# =========== build out tab one fully function =============

def build_tab_1():
    departments = ("BRANDED", "E-STORE", "LTL")
    users = ("EAI111", "EAI222", "EAI333")
    types = ("UOM", "SKU", "WEIGHT")
    return [
        # Manually select metrics
        html.Div(
            id="set-specs-intro-container",
            # className='twelve columns',
            children=html.P(
                "Change settings to view personalized reports "
            ),
        ),
        html.Div(
            id="settings-menu",
            children=[
                html.Div(
                    id="metric-select-menu",
                    # className='five columns',
                    children=[
                        html.Label(id="metric-select-title", children="Select Department"),
                        html.Br(),
                        dcc.Dropdown(id="dept-select",
                                     options=list(
                                         {"label": department, "value": department} for department in departments

                                     ),
                                     value=departments[0],
                                     multi=False,
                                     placeholder="Select a Dept",
                                     style={'width': "100%",
                                            "align-content": "center",
                                            "color": "#003F98", },
                                     ),
                        dcc.Dropdown(id="user-select",
                                     options=list(
                                         {"label": use, "value": use} for use in users

                                     ),
                                     value=users[0],
                                     multi=False,
                                     placeholder="Select a User",
                                     style={'width': "100%",
                                            "align-content": "center",
                                            "color": "#003F98", },
                                     ),
                        dcc.Dropdown(id="type-pick",
                                     options=list(
                                         {"label": typ, "value": typ} for typ in types

                                     ),
                                     value=types[0],
                                     multi=False,
                                     placeholder="Select a View",
                                     style={'width': "100%",
                                            "align-content": "center",
                                            "color": "#003F98", },
                                     ),

                        dcc.DatePickerSingle(
                            id="my-date-picker-single",
                            min_date_allowed=date(1995, 8, 5),
                            max_date_allowed=date(2021, 3, 7),
                            initial_visible_month=date(2021, 3, 7),
                            date=date(2021, 2, 14)
                        ),
                    ],
                ),
                html.Div(
                    id="value-setter-menu",
                    # className='six columns',
                    children=[
                        html.Div(id="value-setter-panel"),
                        html.Br(),
                        html.Div(
                            id="button-div",
                            children=[
                                html.Button("Update", id="value-setter-set-btn"),
                                html.Button(
                                    "View current setup",
                                    id="value-setter-view-btn",
                                    n_clicks=0,
                                ),
                            ],
                        ),
                        html.Div(
                            id="value-setter-view-output", className="output-datatable"
                        ),
                    ],
                ),
            ],
        ),
    ]


# ============ generate modal ==============

def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        ###### What is this app about?

                        This is a dashboard for monitoring user pick information in an supportive, encouraging way.
                        The goal is to provide a more accurate review of employee productivity so we can all make 
                        better informed decisions , and to create a new interesting way to show off what the pickers do 
                        everyday at Epson.

                        ###### What does this app show?

                        It shows individual employees picks creatively sorting by:

                        1). Unit of measure (piece, sub-pack, master-pack, pallet)

                        2). Product type (ink, printer, projector, paper)

                        3). Weight group (0-1pound, 2-5pound, 6-10pound, 11-20pound, 21-40pound, 40-100pound, 100+pound) 

                        4). Time window (select to-from calendar dates)

                        5). Department

                        6). Pick location from zone (general rack/area pick came from)

                        7). And much much more!


                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )


# =========== build tab two fully =================

def build_quick_stats_panel(cal, dep, user_n, typ, t_rate):
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P("USER ID"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value=[user_n],
                        color="#92e0d3",
                        backgroundColor="#1e2130",
                        size=50,
                    ),
                ],
            ),
            html.Div(
                id="card-2",
                children=[
                    html.P("DEPARTMENT"),
                    html.H1(id="department-display", children=[dep],
                            style={'text-align': 'center', "color": "white", "font-family": "Helvetica Neue 55", }),
                    html.P("DATE"),
                    html.H1(id="date-display", children=[cal],
                            style={'text-align': 'center', "color": "white", "font-family": "Helvetica Neue 55", }),
                    html.P("PICK RATE PERCENTAGE"),
                    html.H1(id="pick-rate-display", children=[t_rate],
                            style={'text-align': 'center', "color": "white", "font-family": "Helvetica Neue 55", }),
                ],
            ),
            html.Div(
                id="possible-smileys",
            ),
        ],
    )


# ====== build banner ======


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


# ======== build top right panels =========


def build_top_panel(stopped_interval):
    """
    fig.update_layout(
        legend_bgcolor=(0, 0, 0, 0),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    """
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("Picker Zone Stats Summary"),
                    html.Div(
                        id="metric-div",
                        children=[
                            html.Div(
                                id="metric-rows",
                                children=[],
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                id="ooc-piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("Picks in a Pie"),
                    dcc.Graph(id="pie-chart",

                              figure=px.pie(df, values="qty", names="UOM", color='UOM',
                                            color_discrete_map={'pc': 'lightcyan',
                                                                'sp': 'cyan',
                                                                'mp': 'royalblue',
                                                                'pl': 'darkblue',
                                                                'NO DATA': 'black'}),
                              style={'text-align': "center", "color": "#003F98",
                                     "font-family": "Helvetica Neue 55", "opacity": "85%",
                                     "hoverinfo": "label", "textinfo": "label", }, ),
                ],
            ),
        ],
    )


"""

"""


# ======== build out bottom chart area ==========

def build_chart_panel():
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner("Picks Over Time"),
            dcc.Graph(
                id="bar-graph",
                figure=px.bar(df["time1"]),
            ),
        ],
    )


# ---------------layout ------------------------------------------------------------------------------------------
"""
app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content')
])
"""

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="value-setter-store", data=(init_value_setter_store())),
        dcc.Store(id="n-interval-stage", data=50),
        generate_modal(),
    ],
)

# -----------callbacks-----------------------------------------------------------------------------------
"""
@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
"""


# ===== tab update =========

@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value"), Input("value-setter-store", "data")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, data, stopped_interval):
    if tab_switch == "tab1":
        return build_tab_1(), stopped_interval

    t_rate = data["Rate_Total"]
    cal = data["Date"]
    dep = data["Department"]
    user_n = re.sub('\D', '', data["User"])
    typ = data["Type"]

    return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(cal, dep, user_n, typ, t_rate),
                html.Div(
                    id="graphs-container",
                    children=[build_top_panel(stopped_interval), build_chart_panel()],
                ),
            ],
        ),
        stopped_interval,
    )


# Update interval
@app.callback(
    Output("n-interval-stage", "data"),
    [Input("app-tabs", "value")],
    [
        State("interval-component", "n_intervals"),
        State("interval-component", "disabled"),
        State("n-interval-stage", "data"),
    ],
)
def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
    if disabled:
        print(cur_interval)

        return cur_interval

    if tab_switch == "tab1":
        return cur_interval
    return cur_stage


# ======= Callbacks for modal popup =======
@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}

    return {"display": "none"}


# ==== callback for change filters update graphs ========


@app.callback(
    [Output("department-display", "children"), Output("operator-led", "value"), Output("date-display", "children"),
     Output("pick-rate-display", "children"), Output("metric-rows", "children"),
     Output("bar-graph", "figure"), Output("pie-chart", "figure")],
    inputs=[
        Input("dept-select", "value"),
        Input("user-select", "value"),
        Input("type-pick", "value"),
        Input('my-date-picker-single', 'date')
    ],
)
def settings_changes(department_value, user_value, type_value, date_value):
    df['date'] = df['date'].astype(str)
    print(date_value)
    print(df)
    df_df = df.loc[df["date"] == date_value]
    udf_df = df_df.loc[df["user"] == user_value]
    print(udf_df)
    listy = []
    dicty = {}

    for i in list(udf_df["from_zone"]):
        dicty[i] = i
    for i in dicty.keys():
        listy.append(str(i))

    amount_row_summary = len(listy)

    dict_zones_total_picks = {}

    for zone in dicty:
        new_data = udf_df.loc[df["from_zone"] == zone]
        dict_zones_total_picks[zone] = new_data.shape[0]

    tudf_df = udf_df.loc[df["sku"] == type_value]

    a = department_value
    b = user_value
    c = type_value
    d = date_value

    zone_read_out_1 = html.p = "Zone: DI1 --- PPH: 100 --- Avg PPH: 75 --- Perc Avg: 133% --- Pass/Fail: Pass"
    zone_read_out_2 = html.p = "Zone: DI1 --- PPH: 100 --- Avg PPH: 75 --- Perc Avg: 133% --- Pass/Fail: Pass"

    zone_read_out = (zone_read_out_1, zone_read_out_2)

    # percent of picks picked in each zone you picked in out of the rate average for that zone. so like di is 30pph
    # if you got 45pph in one hour you did 150% add then all up and see what totoal percent you havd.
    # probably do like first pick to last pick is how long in each zone, -- that time versus how many picks where there.
    # there may be alot of zone time values generaged and often we will see 1 pick onlt between each zone.
    # figure this out later
    percent_total = "110%"

    fig_bar = px.bar(udf_df["time1"])

    fig_pie = px.pie(udf_df, values="qty", names="uom", color='uom',
                     color_discrete_map={'pc': 'lightcyan',
                                         'sp': 'cyan',
                                         'mp': 'royalblue',
                                         'pl': 'darkblue',
                                         'NO DATA': 'black'})

    return a, b, d, percent_total, zone_read_out, fig_bar, fig_pie


# ====== Callbacks to update stored data via click =====
@app.callback(
    output=Output("value-setter-store", "data"),
    inputs=[Input("value-setter-set-btn", "n_clicks")],
    state=[
        State("value-setter-store", "data"),
        State("my-date-picker-single", "date"),
        State("dept-select", "value"),
        State("user-select", "value"),
        State("type-pick", "value"),
    ],
)
def set_value_setter_store(set_btn, data, cal, dep, usr, typ):
    print(set_btn)
    if set_btn is None:
        print("none button")
        return data
    else:
        print("yes button 1")
        data["Date"] = cal
        data["Department"] = dep
        data["User"] = usr
        data["Type"] = typ
        return data


@app.callback(
    output=Output("value-setter-view-output", "children"),
    inputs=[
        Input("value-setter-view-btn", "n_clicks"),
        Input("value-setter-store", "data"),
    ],
)
def show_current_specs(n_clicks, store_data):
    print("yes button 2")
    if n_clicks > 0:
        print("yes button 3")
        new_df_dict = {
            "Data Filters": [
                "Current Date Selected",
                "Current Department Selected",
                "Current User Selected",
                "Current Type Selected",
            ],
            "Current Setup": [
                store_data["Date"],
                store_data["Department"],
                store_data["User"],
                store_data["Type"],
            ],
        }
        new_df = pd.DataFrame.from_dict(new_df_dict)
        return dash_table.DataTable(
            style_header={"fontWeight": "bold", "color": "inherit"},
            style_as_list_view=True,
            fill_width=True,
            style_cell_conditional=[
                {"if": {"column_id": "Data Filters"}, "textAlign": "left"}
            ],
            style_cell={
                "backgroundColor": "#1e2130",
                "fontFamily": "Open Sans",
                "padding": "0 2rem",
                "color": "darkgray",
                "border": "none",
            },
            css=[
                {"selector": "tr:hover td", "rule": "color: #91dfd2 !important;"},
                {"selector": "td", "rule": "border: none !important;"},
                {
                    "selector": ".dash-cell.focused",
                    "rule": "background-color: #1e2130 !important;",
                },
                {"selector": "table", "rule": "--accent: #1e2130;"},
                {"selector": "tr", "rule": "background-color: transparent"},
            ],
            data=new_df.to_dict("rows"),
            columns=[{"id": c, "name": c} for c in ["Data Filters", "Current Setup"]],
        )


# ----------- run server -------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
