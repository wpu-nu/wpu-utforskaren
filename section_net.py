from common import *
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import json
import re
from pprint import pprint, pformat
import networkx as nx
from network import *
from functools import partial
from html import unescape
import datetime
import urllib
import base64
import copy

with open("styles.json", "rb") as file:
  stylesheet = json.load(file)
print(__file__)
pprint(stylesheet)

app.layout = dbc.Container(children=[
    dcc.Store(id='local-store', storage_type='local'),
    dbc.Row([
      dbc.Col(
        html.Div(
          id="left-toolbox",
          style={
            "backgroundColor": "#E5EFE5",
            "borderColor": "black",
            "borderStyle": "solid",
            "borderWidth": "1px",
            "height": "90vh",
            "margin": "0px",
            "paddingLeft": "8px",
            "paddingRight": "0px",
            "paddingTop": "8px",
            "paddingBottom": "0px",
            "width": "auto",
            "overflowX": "visible",
            "overflowY": "scroll"
          },
          children=[]),
        width=1,
        className="m-0 p-0"
      ),
      dbc.Col(


            children=
            #dcc.Loading([
              cyto.Cytoscape(
                id='cytoscape-net',
                elements=[],
                layout={
                  'name': 'cola',
                  "convergenceThreshold": 0.0,
                  "edgeLength": 80,
                  "edgeSymDiffLength": 0,
                  "edgeJaccardLength": 500,
                  "unconstrIter": 2000,
                  "userConstIter": 2000,
                  "allConstIter": 2000,
                  # 'animate': 'end',
                  # 'animationEasing': 'easeInOut',
                  # 'numIter': '6000',
                  # 'padding': 0
                  },
                stylesheet=stylesheet,
                style={
                        'height': '90vh',
                        "width": "auto",
                        "borderWidth": "0px",
                        "padding": "0px",
                        "margin": "0px"
                        },
                zoomingEnabled=True,
                zoom=.5,
                maxZoom = 10,
                minZoom = .1,
                #autoRefreshLayout = False
              ),
          #  Space for timelines etc
        width = 8,
        id="cytoscape-net-col",
        className="m-0 p-0"
      ),
      dbc.Col([
        html.Iframe(id="wpu-page-preview",
          style={
                  'height': '90vh',
                  "borderWidth": "0px",
                  "maxWidth": "550px",
                  "minWidth": "400px",
                  "width": "-webkit-fill-available",
                  "padding": "0px",
                  "margin": "0px"
          },
          hidden=False
          )
        ],
        width=3,
        id="wpu-page-preview-col",
        className="m-0 p-0"
      )
    ],
    className="no-gutters"
    ),
    dbc.Row([
      dbc.Col([
        #             dbc.Label("Visa typer"),
        #             dbc.Checklist(
        #                 options=[
        #                     {"label": "Person", "value": "Person"},
        #                     {"label": "Uppslag", "value": "Section"},
        #                     {"label": "Avsnitt", "value": "Chapter"},
        #                     {"label": "Platser", "value": "Place"},
        #                     {"label": "Objekt", "value": "Object"},
        #                 ],
        #                 value=[],
        #                 id="toggle-node-type-visibility",
        #                 switch=True,
        #             ),

         ],
        width=2,
        className="m-0 p-2"
      ),
      dbc.Col([
        # dbc.Label("Visa relationer"),
        # dbc.Checklist(
        #     options=[
        #         {"label": "[Uppslag] anknyter [uppslag]", "value": "Section_RelatesTo_Section"},
        #         {"label": "[Person] känner [person]", "value": "Person_Knows_Person"},
        #         {"label": "[Person] förhörd av [person]", "value": "Person_WasInterrogatedBy_Person"},
        #         {"label": "[Person] förhörd i [uppslag]", "value": "Person_WasInterrogatedIn_Section"},
        #         {"label": "[Person] omnämnd i [uppslag]", "value": "Person_MentionedIn_Section"},
        #     ],
        #     value=[],
        #     id="toggle-edge-type-visibility",
        #     switch=True,
        # ),
        ],
        width=2,
        className="m-0 p-2"
      ),
      dbc.Col([
          dbc.InputGroup(
            [
            dbc.Input(id='search-text-input', value="", placeholder="Stig Engström"),
            dbc.Button("Sök", id="search-button"),
            ])
        ], width=3,
        className="m-0 p-2"
      ),
      dbc.Col(children=[
                html.A(id='download-network', download="network-data.json", href="", target="_blank", hidden=False,
                  children=[
                    dbc.Button("Spara nätverk", id="export-network-button", className="btn btn-primary btn-sm m-1 p-1"),
                  ]
                ),
                dcc.Upload(
                  id='upload-network',
                  children=[
                    dbc.Button("Öppna nätverk", id="load-network-button", className="btn btn-primary btn-sm m-1 p-1")
                  ]
                ),

                dbc.Button("Radera nätverk", id="delete-local-storage-button", className="btn btn-warning btn-sm m-1 p-1")
        ],
        width=1,
        className="m-0 p-2"
      ),
      dbc.Col(
              children=[
                dbc.InputGroup(
                  [dbc.InputGroupAddon("Layout", addon_type="prepend"),
                    dbc.DropdownMenu([
                    dbc.DropdownMenuItem('Slumpmässig', id='layout-algo-select-random'),
                    dbc.DropdownMenuItem('Rutnät', id='layout-algo-select-grid'),
                    dbc.DropdownMenuItem('Cirkel', id='layout-algo-select-circle'),
                    dbc.DropdownMenuItem('Concentrisk', id='layout-algo-select-concentric'),
                    dbc.DropdownMenuItem('Bredden-först', id='layout-algo-select-breadthfirst'),
#                    dbc.DropdownMenuItem('FCose', id='layout-algo-select-fcose'),
                    dbc.DropdownMenuItem('Cose', id='layout-algo-select-cose'),
                    dbc.DropdownMenuItem('Cose-bilkent', id='layout-algo-select-cose-bilkent'),
                    dbc.DropdownMenuItem('Dagre', id='layout-algo-select-dagre'),
                    dbc.DropdownMenuItem('Cola', id='layout-algo-select-cola'),
                    dbc.DropdownMenuItem('Klay', id='layout-algo-select-klay'),
                    dbc.DropdownMenuItem('Sprid ut', id='layout-algo-select-spread'),
                    dbc.DropdownMenuItem('Euler', id='layout-algo-select-euler'),
                  ],
                  label="Cola",
                  direction="up",
                  id='layout-algo-select',
                  ),
                ],
                size="sm",
                className="m-1 p-1",
              ),
              dbc.InputGroup(
                [
                  dbc.InputGroupAddon("Spara bild", addon_type="prepend"),
                    dbc.DropdownMenu([
                      dbc.DropdownMenuItem('PNG', id={'role': 'export-image', 'type': 'png'}),
                      dbc.DropdownMenuItem('JPG', id={'role': 'export-image', 'type': 'jpg'}),
                      dbc.DropdownMenuItem('SVG', id={'role': 'export-image', 'type': 'svg'}),
                    ],
                    label="PNG",
                    direction="up",
                    id='export-image-select',
                    ),
                ]),
          ],
          width=3,
        className="m-0 p-2"
        ),
      dbc.Col([
        dbc.Button("Dölj wpu-artiklar", id="hide-wpu-preview-button", className="btn btn-primary btn-sm m-1 p-1"),
        dbc.Button("Expandera alla noder", id="expand-all-nodes-button", className="btn btn-primary btn-sm m-1 p-1")
      ],
      width=1,
      className="m-0 p-2"
      )
      ],
      className="no-gutters"
      ),
    #   ]
    # ),
    html.Div(id='add-node-signal', children="", hidden=True),
    html.Div(id='add-node-nbrs-signal', children="", hidden=True),
    dcc.Location(id='url', refresh=False),
    dbc.Modal([
      dbc.ModalHeader("Sökresultat"),
      dbc.ModalBody(children=[
        html.Div("Här visas endast de sökträffar som går att lägga till. Det betyder att det måste finnas en uppslagssida eller personsida."),
        html.Hr(),
        html.Div(id="search-results-area", children=[])
      ]),
      dbc.ModalFooter(dbc.Button("Stäng", id="close-search-results-modal", className="ml-auto"))
    ],
    id="search-results-modal",
    size="lg",
    ),
  ],
  fluid=True,
  className="m-0 p-0"
)

@app.callback(Output("cytoscape-net", "generateImage"),
              Input({'role': "export-image", 'type': ALL}, "n_clicks"))
def generate_image(n_clicks):
  ctx = dash.callback_context
  if not ctx.triggered:
    return dash.no_update

  button_id = ctx.triggered[0]['prop_id'].split('.')[0]
  prop_id = ctx.triggered[0]['prop_id'].split('.')[1]
  button_id = json.loads(button_id)
  if "role" in button_id and button_id["role"] == "export-image":
    filename = "wpu-utforskaren_" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    return {"type": button_id["type"], "action": "download", "filename": filename}

  return dash.no_update





@app.callback([Output("search-results-modal", "is_open"),
              Output("search-results-area", "children")],
             [Input("close-search-results-modal", "n_clicks"),
              Input("search-button", "n_clicks")],
              State("search-text-input", "value"))
def search_results_modal(close_clicks, search_clicks, search_text):
  print(__file__, "search_results_modal")

  ctx = dash.callback_context
  if not ctx.triggered:
    return dash.no_update

  button_id = ctx.triggered[0]['prop_id'].split('.')[0]

  if button_id == "close-search-results-modal":
    return [False, ""]
  elif button_id == "search-button" and len(search_text.strip().strip(".-:,")) > 0:
    net = get_wpu_connectome_nx()
    max_results = 10
    results_layout = []
    for result in wpu.search(search_text, limit=100):
      if node_exists_in_wpu(result['title']):
        snippet = unescape(result["snippet"].replace('<span class="searchmatch">', "").replace("</span>", ""))
        results_layout.append(html.Div([
            html.A(href=f"https://wpu.nu/wiki/{result['title']}", target="_blank", children=result['title']),
            html.I(children=html.P(children=snippet)),
            dbc.Button("Lägg till", id={'role': "add-search-result-button", 'name': result['title']} , className="btn btn-primary btn-sm"),
            html.Hr()
          ]))
        if len(results_layout) > 10:
          break
    return [True, results_layout]
  else:
    return [False, dash.no_update]


@app.callback(Output('add-node-signal', 'children'),
  [
    Input({'role': 'add-this-node-button', 'node': ALL}, 'n_clicks'),
    Input({"role": "add-search-result-button", "name": ALL}, "n_clicks"),
  ])
def add_node_click(add_this_node, add_searched_node):
  # Adds node :)
  # The dynamic left hand toolbox adds a bit of complexity here
  ctx = dash.callback_context
  if not ctx.triggered:
    return dash.no_update
  button_id = ctx.triggered[0]['prop_id'].split('.')[0]

  if "add-this-node-button" in button_id:
    button_id = json.loads(button_id)
    if "role" in button_id and button_id["role"] == "add-this-node-button":
      if len(set(add_this_node)) == 1 and add_this_node[0] is None: # disable triggering on creation
        return dash.no_update
      else:
        return button_id["node"]
    else:
      return dash.no_update

  elif "add-search-result-button" in button_id:
    button_id = json.loads(button_id)
    if "name" in button_id and button_id["role"] == "add-search-result-button":
      if len(set(add_searched_node)) == 1 and add_searched_node[0] is None: # disable triggering on creation
        return dash.no_update
      else:
        return add_type(button_id["name"])
    else:
      return dash.no_update
  else:
    return dash.no_update




@app.callback(
    [
    Output("cytoscape-net", "layout"),
    Output("layout-algo-select", "label"),
    ],
    [
    Input("layout-algo-select-circle", "n_clicks"),
    Input('layout-algo-select-random',"n_clicks"),
    Input('layout-algo-select-grid',"n_clicks"),
    Input('layout-algo-select-concentric',"n_clicks"),
    Input('layout-algo-select-breadthfirst',"n_clicks"),
    #Input('layout-algo-select-fcose',"n_clicks"),
    Input('layout-algo-select-cose',"n_clicks"),
    Input('layout-algo-select-cose-bilkent',"n_clicks"),
    Input('layout-algo-select-dagre',"n_clicks"),
    Input('layout-algo-select-cola',"n_clicks"),
    Input('layout-algo-select-klay',"n_clicks"),
    Input('layout-algo-select-spread',"n_clicks"),
    Input('layout-algo-select-euler',"n_clicks"),
    ],
    [
    State("cytoscape-net", "layout"),
    State("layout-algo-select", "label")
    ]
)
def set_cyto_layout(
            layout_algo_select_circle_clicks,
            layout_algo_select_random_clicks,
            layout_algo_select_grid_clicks,
            layout_algo_select_concentric_clicks,
            layout_algo_select_breadthfirst_clicks,
            #layout_algo_select_fcose_clicks,
            layout_algo_select_cose_clicks,
            layout_algo_select_cose_bilkent_clicks,
            layout_algo_select_dagre_clicks,
            layout_algo_select_cola_clicks,
            layout_algo_select_klay_clicks,
            layout_algo_select_spread_clicks,
            layout_algo_select_euler_clicks,
            layout, label):
  ctx = dash.callback_context
  if not ctx.triggered:
    return [layout, label]

  print(__file__, ctx.triggered[0]['prop_id'].split('.')[0])
  layout["name"] = ctx.triggered[0]['prop_id'].split('.')[0].replace("layout-algo-select-", "")
  if layout["name"] == "cola":
    layout["convergenceThreshold"] = 0.0
    layout["edgeLength"] = 80
    #layout["edgeSymDiffLength"] = 0
    layout["edgeJaccardLength"] = 500
    layout["unconstrIter"] = 2000
    layout["userConstIter"] = 2000
    layout["allConstIter"] = 2000


  label = layout["name"]

  return [layout, label]


def get_network_download_data(data):
  d = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
  return "data:application/json;charset=utf-8," + urllib.parse.quote(d)

@app.callback(Output(component_id='download-network', component_property='download'),
              Input(component_id='download-network', component_property='href'))
def update_download_network_filename(href):
  filename = "wpu-utforskaren_" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + ".json"
  return filename


def filter_edges(local_store_data, n1, n2, n3):
  # matches the edges in local store with edges and nodes in nx
  if local_store_data is None or "include" not in local_store_data or "edges" not in local_store_data["include"]:
    return False

  if n1 in local_store_data["include"]["nodes"] and n2 in local_store_data["include"]["nodes"]:
    return True

  return False


def filter_nodes(local_store_data, n):
  # matches the nodes in local store with nodes in nx
  return local_store_data is not None and "include" in local_store_data and "nodes" in local_store_data["include"] and n in local_store_data["include"]["nodes"]

@app.callback(
            [Output('cytoscape-net', 'elements'),
            Output(component_id='download-network', component_property='href')],
            [Input('cytoscape-net', 'mouseoverNodeData'),
             Input('cytoscape-net', 'mouseoverEdgeData'),
             Input('local-store', 'clear_data'),
             Input('local-store', 'modified_timestamp')
             ],
             [State('local-store', 'data'),
              State('cytoscape-net', 'elements')])
def display_cyto(hover_node, hover_edge, clear_data, timestamp, local_store_data, elements):
  # Handles display of network.
  # Filters out nodes present in local store from nx
  # Changes style on mouse over


  ctx = dash.callback_context
  if not ctx.triggered:
    return [elements, get_network_download_data(local_store_data)]
  trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
  trigger_prop = ctx.triggered[0]['prop_id'].split('.')[1]
  print(__file__, f"{ctx.triggered[0]=}")
  if trigger_id == "cytoscape-net":
    if trigger_prop == "mouseoverNodeData":
      #print(__file__, f"{hover_node=}")
      for idx, node in enumerate(elements["nodes"]):
        if "classes" not in elements["nodes"][idx]:
          elements["nodes"][idx]["classes"] = ""
        if node["data"]["id"] == hover_node["id"]:
          elements["nodes"][idx]["classes"] += " node-hover"
        else:
          elements["nodes"][idx]["classes"] = elements["nodes"][idx]["classes"].replace(" node-hover", "")

      for idx, edge in enumerate(elements["edges"]):
        if "classes" not in elements["edges"][idx]:
          elements["edges"][idx]["classes"] = ""

        if edge["data"]["target"] == hover_node["id"] or edge["data"]["source"] == hover_node["id"]:
          elements["edges"][idx]["classes"] += " edge-hover"
        else:
          elements["edges"][idx]["classes"] = elements["edges"][idx]["classes"].replace(" edge-hover", "")



    elif trigger_prop == "mouseoverEdgeData":
      #print(__file__, f"{hover_edge=}")
      for idx, node in enumerate(elements["nodes"]):
        if "classes" not in elements["nodes"][idx]:
          elements["nodes"][idx]["classes"] = ""
        if node["data"]["id"] == hover_edge["source"] or node["data"]["id"] == hover_edge["target"]:
          elements["nodes"][idx]["classes"] += " node-hover"
        else:
          elements["nodes"][idx]["classes"] = elements["nodes"][idx]["classes"].replace(" node-hover", "")

      for idx, edge in enumerate(elements["edges"]):
        if "classes" not in elements["edges"][idx]:
          elements["edges"][idx]["classes"] = ""

        if edge["data"]["id"] == hover_edge["id"]:
          elements["edges"][idx]["classes"] += " edge-hover"
        else:
          elements["edges"][idx]["classes"] = elements["edges"][idx]["classes"].replace(" edge-hover", "")


    return [elements, get_network_download_data(local_store_data)]


  if  trigger_prop != "clear_data" and timestamp == -1:
    return [dash.no_update,  get_network_download_data(local_store_data)]
  mg = get_wpu_connectome_nx()


  mg_filtered = nx.classes.graphviews.subgraph_view(mg, filter_node=partial(filter_nodes, local_store_data), filter_edge=partial(filter_edges, local_store_data))
  print(__file__, f"Investigation network size: {mg.number_of_nodes()} nodes and {mg.number_of_edges()} edges")
  print(__file__, f"Display network size: {mg_filtered.number_of_nodes()} nodes and {mg_filtered.number_of_edges()} edges")

  m = nx.readwrite.json_graph.cytoscape_data(mg_filtered)
  if type(local_store_data) == dict and "highlight" in local_store_data:
    for idx, edge in enumerate(m["elements"]["edges"]):

      if edge["data"]["id"] in local_store_data["highlight"]["edges"]:
        m["elements"]["edges"][idx]["classes"] = "edge-highlighted"
      else:
        m["elements"]["edges"][idx]["classes"] = ""


  return [m["elements"],  get_network_download_data(local_store_data)]




@app.callback(
   Output(component_id='local-store', component_property='data'),
   [Input(component_id='add-node-signal', component_property='children'),
    Input(component_id='add-node-nbrs-signal', component_property='children'),
    Input(component_id='expand-all-nodes-button', component_property='n_clicks'),
    Input(component_id='url', component_property='pathname'),
    Input(component_id='cytoscape-net', component_property='tapEdgeData'),
    Input(component_id={'role': 'remove-node-button', 'dummy': ALL}, component_property='n_clicks'),
    Input(component_id='upload-network', component_property='contents'),
    Input(component_id='upload-network', component_property='last_modified')],
    [
    State(component_id='local-store', component_property='modified_timestamp'),
    State(component_id='local-store', component_property='data'),
    State(component_id={'role': 'add-all-nbrs-data', 'dummy': ALL}, component_property='children')]
   ) # @cache.memoize(timeout=7200)
def modify_network(node_to_add, node_to_add_nbrs, expand_all_nodes, url, tapped_edge, remove_node_button, uploaded_data, upload_timestamp, local_store_timestamp, local_store_data, node_to_remove):

  # Add nodes from various inputs, outputs to local store that in turn triggers display cyto

  ctx = dash.callback_context
  if not ctx.triggered:
    return dash.no_update
  trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
  trigger_prop = ctx.triggered[0]['prop_id'].split('.')[1]

  print("modify_network")
  print(trigger_id, trigger_prop)
  if trigger_id == "upload-network":
    print("Loading network from file")
    pprint(uploaded_data)
    data = uploaded_data.split(',')[-1]
    pprint(data)
    local_store_data = json.loads(base64.b64decode(data))
    pprint(local_store_data)
    return local_store_data

  local_store_data_before = str(local_store_data)

  if local_store_timestamp == -1 and (local_store_data is None or local_store_data == "" or local_store_data == [] or local_store_data == {}):
    local_store_data =  {"include": {"nodes": [], "edges": []}, "highlight": {"edges": [], "nodes": []}}
    return local_store_data

  if "remove-node-button" in trigger_id and remove_node_button != [None]:
    trigger_id_json = json.loads(trigger_id)
    if trigger_id_json["role"] == "remove-node-button":
      if node_to_remove != "" and node_to_remove != [] and node_to_remove is not None:
        if type(node_to_remove) == list:
          node_to_remove = node_to_remove[0]
        print("removing:")
        pprint(node_to_remove)
        local_store_data["include"]["nodes"] = [e for e in local_store_data["include"]["nodes"] if node_to_remove != e]
        local_store_data["highlight"]["nodes"] = [e for e in local_store_data["highlight"]["nodes"] if node_to_remove != e]

        local_store_data["include"]["edges"] = [e for e in local_store_data["include"]["edges"] if node_to_remove not in e]
        local_store_data["highlight"]["edges"] = [e for e in local_store_data["highlight"]["edges"] if node_to_remove not in e]

        return local_store_data

  elif trigger_id == "add-node-signal":
    local_store_data["include"]["nodes"].append(node_to_add)
    return local_store_data

  elif trigger_id == "add-node-nbrs-signal":
    print(__file__, f"Neighbouring nodes to {node_to_add_nbrs}")
    mg = get_wpu_connectome_nx()
    for n in mg.neighbors(node_to_add_nbrs):
      print(__file__, "Adding:")
      pprint(n)
      local_store_data["include"]["nodes"].append(n)
      esd = mg[node_to_add_nbrs][n]
      for ed in esd.values():
        pprint(ed)
        local_store_data["include"]["edges"].append(ed["id"])
    return local_store_data

  elif trigger_id == "expand-all-nodes-button" and expand_all_nodes is not None:
    mg = get_wpu_connectome_nx()
    orig_node_list = copy.copy(local_store_data["include"]["nodes"])
    for node_in_dash in orig_node_list:
      print("Processing")
      pprint(node_in_dash)
      for n in mg.neighbors(node_in_dash):
        print(__file__, "Adding:")
        pprint(n)
        local_store_data["include"]["nodes"].append(n)
        esd = mg[node_in_dash][n]
        for ed in esd.values():
          local_store_data["include"]["edges"].append(ed["id"])
    return local_store_data



  elif trigger_id == "url":
    m = re.match(r"/(\w+)/([\w-]+:)?([\w-]+)/?", url)
    if m:
      action = m.group(1)
      ntype = m.group(2)
      name = m.group(3)

      if ntype == "" or ntype is None:
        typed_name = add_type(name)
      else:
        typed_name = f"{ntype}{name}"

      #print(__file__, action, ntype, name, typed_name)
      if action == "add":
        local_store_data["include"]["nodes"].append(typed_name)
        local_store_data["include"]["nodes"] == list(set(local_store_data["include"]["nodes"]))
        return local_store_data



  elif trigger_id == "cytoscape-net" and type(local_store_data) == dict :

    if "highlight" not in local_store_data:
      local_store_data["highlight"] = {"edges": [], "nodes": []}

    if tapped_edge["id"] in local_store_data["highlight"]["edges"]:
      local_store_data["highlight"]["edges"].remove(tapped_edge["id"])
    else:
      local_store_data["highlight"]["edges"].append(tapped_edge["id"])

    local_store_data["highlight"]["edges"] = list(set(local_store_data["highlight"]["edges"]))


  # stinks a bit, but I think this is needed to avoid null-updates
  if local_store_data_before == str(local_store_data):
    return dash.no_update

  return local_store_data


@app.callback(Output('local-store', 'clear_data'),
              Input('delete-local-storage-button', 'n_clicks'))
def clear_data(n_clicks):
  # Clears local data
  return (n_clicks is not None and n_clicks > 0)


@app.callback(Output('left-toolbox', 'children'),
              Input('cytoscape-net', 'tapNodeData'),
              State(component_id='local-store', component_property='data'))
def node_selected(tapped_node, local_store_data):
  # Populates left side toolbox
  if tapped_node is not None and tapped_node != {} and tapped_node != "":

    toolbar_layout = [html.Div(style={"fontSize": "12px"},
        children=[
          html.A(href=tapped_node["url"], target="_blank", children=html.H3(tapped_node["name"])),
          html.Br(),
          dbc.Button("Ta bort", className="btn-sm btn-warning align-self-end", style={"padding": "2px"}, id={'role': 'remove-node-button', 'dummy': '<- im with stupid'}),
          html.Div(id={'role': "add-all-nbrs-data", "dummy": "<- im with stupid"}, hidden=True, children=tapped_node["id"]),
          dbc.Button("Lägg till allt", className="btn-sm align-self-end", style={"padding": "2px"}, id={'role': 'add-all-nbrs-button', 'dummy': '<- im with stupid'}),
          ]
        )
    ]
    print(__file__, f"Neighbouring nodes to {tapped_node['name']}")
    mg = get_wpu_connectome_nx()
    edge_layouts = {}
    try:
      targets = []
      for n in mg.neighbors(tapped_node["id"]):

        esd = mg[tapped_node["id"]][n]
        for ed in esd.values():
          target_node = mg.nodes[n]
          if ed["type"] not in edge_layouts.keys():
            edge_layouts[ed["type"]] = [html.Br(), html.H6(queries[ed["type"]]["plain_text"].capitalize())]

          target = target_node["type"]+":"+target_node["name"]
          if target in targets:
            continue
          targets.append(target)
          if target not in local_store_data["include"]["nodes"]:
            edge_layouts[ed["type"]].append(
                  html.Li([
                    html.A(target_node["name"], target="_blank", href=target_node["url"]),
                    dbc.Button("Lägg till", className="btn-sm align-self-end", style={"padding": "2px"}, id={'role': "add-this-node-button", "node": f"{n}"}),
                  ],
                 style={"fontSize": "12px"})
                 )
          else:
            edge_layouts[ed["type"]].append(
                  html.Li([
                    html.A(target_node["name"], target="_blank", href=target_node["url"]),
                  ],
                 style={"fontSize": "12px"})
                 )

    except nx.exception.NetworkXError:
      print(__file__, "Node not in graph")

    for elk in sorted(edge_layouts.keys()):
      for e in edge_layouts[elk]:
        toolbar_layout.append(e)

    return toolbar_layout
  else:
    return dash.no_update



def add_type(node_text):
  # Heuristics to deduct type for search string
  if ":" in node_text:
    node_type = node_text.split(":")[0].strip().capitalize()
    node_name = node_text.split(":")[1].strip()
  else:
    node_name = node_text
    if "-" not in node_text:
      node_type = "Person"
    else:
      if len([1 for d in "0123456789" if d in node_text]) > 0:
        # dash and number, probably a section code
        node_type = "Section"
      else:
        node_type = "Person"
  return node_type + ":" + node_name



@app.callback(Output('add-node-nbrs-signal', 'children'),
    Input({'role': 'add-all-nbrs-button', "dummy": ALL}, 'n_clicks'),
    State({'role': 'add-all-nbrs-data', "dummy": ALL}, 'children'),
  )
def add_node_nbrs_click(add_all_neighbours_clicks, add_all_neighbours_data):

  ctx = dash.callback_context
  if not ctx.triggered:
    return dash.no_update

  button_id = ctx.triggered[0]['prop_id'].split('.')[0]
  print(__file__, button_id)

  if type(add_all_neighbours_clicks) == list and len(add_all_neighbours_clicks) > 0:
    add_all_neighbours_clicks = add_all_neighbours_clicks[0]

  if type(add_all_neighbours_data) == list and len(add_all_neighbours_data) > 0:
    add_all_neighbours_data = add_all_neighbours_data[0]


  if "add-all-nbrs-button" in button_id:
    button_id = json.loads(button_id)
    if "role" in button_id and button_id["role"] == "export-image":

      if add_all_neighbours_clicks is None or add_all_neighbours_clicks < 1:
        return dash.no_update

    if add_all_neighbours_data != "":
      print(__file__, f"Add all neighbours to {add_all_neighbours_data}")
      return add_all_neighbours_data

  return dash.no_update


@app.callback(Output('wpu-page-preview', 'src'),
              Input('cytoscape-net', 'tapNodeData'))
def display_tap_node_data(data):
  # Show right hand side iframe
  if data is None:
    return "https://wpu.nu/wiki/wpu-utforskaren"
  if 'url' not in data:
    return "https://wpu.nu/wiki/wpu-utforskaren"
  return data['url']


@app.callback([
              Output('wpu-page-preview', 'hidden'),
              Output('hide-wpu-preview-button', 'children'),
              Output('cytoscape-net-col', 'width'),
              Output('wpu-page-preview-col', 'width'),
              ],
              Input('hide-wpu-preview-button', 'n_clicks'),
              State('wpu-page-preview', 'hidden'))
def expand_graph_area(button_clicks, is_hidden):
  # Hide right hand side preview
  if button_clicks is None or button_clicks < 1:
    return [False, "Göm wpu-artiklar", 9, 2]
  elif is_hidden == True:
    return [False, "Göm wpu-artiklar", 9, 2]
  else:
    return [True, "Visa wpu-artiklar", 11, 0]

get_wpu_connectome_nx(skip_saved=False)
server = app.server   # for gunicorn
if __name__ == '__main__':
  app.run_server(host="0.0.0.0", port=5001, debug=True, dev_tools_hot_reload=True, dev_tools_hot_reload_interval=1, dev_tools_hot_reload_watch_interval=1, dev_tools_silence_routes_logging=True)
