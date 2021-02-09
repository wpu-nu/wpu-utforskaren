from common import *
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import json
import re
from pprint import pprint
import networkx as nx
from network import *
from functools import partial

with open("styles.json", "rb") as file:
  stylesheet = json.load(file)
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
            "height": "95vh",
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
                        'height': '95vh',
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
                  'height': '95vh',
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
            dbc.Input(id='add-node-text-input', value="", placeholder="Person:Stig Engström"),
            dbc.Button("Lägg till", id="add-node-button"),
            ])
        ], width=3,
        className="m-0 p-2"
      ),
      dbc.Col(children=[
                dbc.Button("Radera sparat", id="delete-local-storage-button", className="btn btn-warning btn-sm")
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
              ),
              ],

        width=3,
        className="m-0 p-2"),
      dbc.Col([
        dbc.Button("Dölj wpu-artiklar", id="hide-wpu-preview-button", className="btn btn-primary btn-sm")
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
  ],
  fluid=True,
  className="m-0 p-0"
)


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

  print(ctx.triggered[0]['prop_id'].split('.')[0])
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


@app.callback(Output('cytoscape-net', 'elements'),
            [Input('cytoscape-net', 'mouseoverNodeData'),
             Input('cytoscape-net', 'mouseoverEdgeData'),
             Input('local-store', 'modified_timestamp')],
             [State('local-store', 'data'),
              State('cytoscape-net', 'elements')])
def display_cyto(hover_node, hover_edge, timestamp, local_store_data, elements):
  # Handles display of network.
  # Filters out nodes present in local store from nx
  # Changes style on mouse over


  ctx = dash.callback_context
  if not ctx.triggered:
    return elements
  trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
  trigger_prop = ctx.triggered[0]['prop_id'].split('.')[1]
  print(f"{ctx.triggered[0]=}")
  if trigger_id == "cytoscape-net":
    if trigger_prop == "mouseoverNodeData":
      #print(f"{hover_node=}")
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
      #print(f"{hover_edge=}")
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


    return elements


  if timestamp == -1:
    return dash.no_update
  mg = get_wpu_connectome_nx()


  mg_filtered = nx.classes.graphviews.subgraph_view(mg, filter_node=partial(filter_nodes, local_store_data), filter_edge=partial(filter_edges, local_store_data))
  print(f"Investigation network size: {mg.number_of_nodes()} nodes and {mg.number_of_edges()} edges")
  print(f"Display network size: {mg_filtered.number_of_nodes()} nodes and {mg_filtered.number_of_edges()} edges")

  m = nx.readwrite.json_graph.cytoscape_data(mg_filtered)
  if "highlight" in local_store_data:
    for idx, edge in enumerate(m["elements"]["edges"]):

      if edge["data"]["id"] in local_store_data["highlight"]["edges"]:
        m["elements"]["edges"][idx]["classes"] = "edge-highlighted"
      else:
        m["elements"]["edges"][idx]["classes"] = ""


  return m["elements"]




@app.callback(
    Output(component_id='local-store', component_property='data'),
   [Input(component_id='add-node-signal', component_property='children'),
    Input(component_id='add-node-nbrs-signal', component_property='children'),
    Input(component_id='url', component_property='pathname'),
    Input(component_id='cytoscape-net', component_property='tapEdgeData')],
    State(component_id='local-store', component_property='modified_timestamp'),
    State(component_id='local-store', component_property='data')
   ) # @cache.memoize(timeout=7200)
def add_nodes(node_to_add, node_to_add_nbrs, url, tapped_edge, local_store_timestamp, local_store_data):

  # Add nodes from various inputs, outputs to local store that in turn triggers display cyto

  local_store_data_before = str(local_store_data)

  if local_store_timestamp == -1 and (local_store_data is None or local_store_data == "" or local_store_data == [] or local_store_data == {}):
    local_store_data =  {"include": {"nodes": [], "edges": []}, "highlight": {"edges": [], "nodes": []}}
    return local_store_data

  if node_to_add is None or local_store_timestamp is None or url is None or local_store_data is None:
    raise PreventUpdate



  ctx = dash.callback_context
  if not ctx.triggered:
    return dash.no_update
  trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

  if trigger_id == "add-node-signal":
    local_store_data["include"]["nodes"].append(node_to_add)

  elif trigger_id == "add-node-nbrs-signal":
    print(f"Neighbouring nodes to {node_to_add_nbrs}")
    mg = get_wpu_connectome_nx()
    for n in mg.neighbors(node_to_add_nbrs):
      print("Adding:")
      pprint(n)
      local_store_data["include"]["nodes"].append(n)
      esd = mg[node_to_add_nbrs][n]
      for ed in esd.values():
        pprint(ed)
        local_store_data["include"]["edges"].append(ed["id"])



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

      #print(action, ntype, name, typed_name)
      if action == "add":
        local_store_data["include"]["nodes"].append(typed_name)
        local_store_data["include"]["nodes"] == list(set(local_store_data["include"]["nodes"]))



  elif trigger_id == "cytoscape-net":

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
  # Clears local data. No effect until browser window is refreshed.
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
          html.Div(id={'role': "add-all-nbrs-data"}, hidden=True, children=tapped_node["id"]),
          dbc.Button("Lägg till allt", className="btn-sm align-self-end", style={"padding": "2px"}, id={'role': 'add-all-nbrs-button'}),
          ]
        )
    ]
    print(f"Neighbouring nodes to {tapped_node['name']}")
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
      print("Node not in graph")

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


@app.callback(Output('add-node-signal', 'children'),
  [
    Input('add-node-button', 'n_clicks'),
    Input({'role': 'add-this-node-button', 'node': ALL}, 'n_clicks'),
  ],
  [
    State('add-node-text-input', 'value')
  ])
def add_node_click(add_node_button_clicks, add_this_node, node_text):
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

  if add_node_button_clicks is None or add_node_button_clicks < 1:
    return dash.no_update

  return add_type(node_text)


@app.callback(Output('add-node-nbrs-signal', 'children'),
    Input({'role': 'add-all-nbrs-button'}, 'n_clicks'),
    State({'role': 'add-all-nbrs-data'}, 'children'),
  )
def add_node_nbrs_click(add_all_neighbours_clicks, add_all_neighbours_data):
  print("add_node_nbrs_click")
  ctx = dash.callback_context
  if not ctx.triggered:
    return dash.no_update

  button_id = ctx.triggered[0]['prop_id'].split('.')[0]
  print(button_id)

  if add_all_neighbours_clicks is None or add_all_neighbours_clicks < 1:
    return dash.no_update

  if button_id == '{"role":"add-all-nbrs-button"}':
    if add_all_neighbours_data != "":
      print(f"Add all neighbours to {add_all_neighbours_data}")
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

server = app.server   # for gunicorn
if __name__ == '__main__':
  app.run_server(host="0.0.0.0", port=5001, debug=True, dev_tools_hot_reload=True, dev_tools_hot_reload_interval=1, dev_tools_hot_reload_watch_interval=1, dev_tools_silence_routes_logging=True)
