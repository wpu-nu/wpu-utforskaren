import networkx as nx
from pprint import pprint
import time

from urllib.parse import unquote
from common import *
import dill as pickle
from pathlib import Path
import re



def wpu_fold_name(name):
  return name.replace(" ", "_")

all_icons = {}
def prefetch_all_person_icons():

  global all_icons

  images = wpu.allimages()

  for image in images:
    #pprint(image.imageinfo)
    name = unquote(image.imageinfo["descriptionurl"])
    name = name.split("Fil:")[-1]
    m = re.match(r"avatar_(.*)\.(?:png|jpg|jpeg)", name, re.IGNORECASE)
    if m:
      person = m.group(1).strip()
      all_icons[person] = unquote(image.imageinfo["url"])
  pprint(all_icons)

def get_person_icon_url_prefetched(person):
  return all_icons.get(wpu_fold_name(person), all_icons["missing"])

@cache.memoize(timeout=7200)
def get_person_icon_url(person):

  for extension in ["png", "jpg", "jpeg"]:
    print(f"Looking for Avatar_{person}.{extension}")
    icon_file = wpu.images[f"Avatar_{person}.{extension}"]
    if "url" in icon_file.imageinfo:
      break
  else:
    return ""
    icon_file = wpu.images["Avatar_missing.png"]


  return unquote(icon_file.imageinfo["url"])


@cache.memoize(timeout=3600)
def node_exists_in_wpu(node_name):

  queries = [f"[[{node_name}]] [[Kategori:Person]]",
             f"[[{node_name}]] [[Kategori:Uppslag]]"]

  for query in queries:
    results = wpu.raw_api('ask', query=f"{query}|limit=100", http_method='GET')
    wpu.handle_api_result(results)  # raises APIError on error

    answers = results['query'].get('results')
    for answer in answers:
      if answer == node_name:
        return True

  return False



@cache.memoize(timeout=3600)
def get_wpu_connectome_dash():
  return nx.readwrite.json_graph.cytoscape_data(get_wpu_connectome_nx())

@cache.memoize(timeout=300)
def get_wpu_connectome_nx():

  pickles = Path("wpu-network.pkl")
  if pickles.is_file():
    with open(str(pickles), "rb") as file:
      print("Unpickling connectome")
      return pickle.load(file)

  print("No pickle find for connectome, querying wpu...")
  prefetch_all_person_icons()



  mg = nx.MultiGraph()
  import collections
  c = 0
  for query_name, query_info in queries.items():
    pprint(query_info)

    results = wpu.raw_api('ask', query=f'{query_info["query"]}|limit=100000000', http_method='GET', retry_timeout=180)
    wpu.handle_api_result(results)  # raises APIError on error

    answers = results['query'].get('results')
    if answers == []:
      print("No answers")
      break

    for answer in answers.values():
      c += 1
      if query_info["source_type"] != "Section":
        source_node_id = query_info["source_type"] + ":" + answer['fulltext']
        source_node_name = answer['fulltext']
      else:
        source_node_id = answer['fulltext'].replace("Uppslag:", "Section:")
        source_node_name = answer['fulltext'].replace("Uppslag:", "")

      mg.add_node(source_node_id, name=source_node_name, type=query_info["source_type"], url=unquote(answer["fullurl"]))

      if query_info["query"] == "Person":
        mg.nodes[source_node_id]['icon_url'] = get_person_icon_url_prefetched(source_node_name)

      if answer["printouts"] != []:
        for edge_type, vals in answer["printouts"].items():
          for val in vals:


            target_node_url = unquote(val['fullurl'])
            target_node_name = val['fulltext'] if query_info["target_type"] != "Section" else val['fulltext'].replace("Uppslag:", "")

            #print(f"{source_node_id} -> {target_node_name}")

            if query_info["target_type"] == "Section" and "Uppslag:" not in target_node_url:
              target_node_url = f"https://wpu.nu/Uppslag:{target_node_name}"

            target_node_id = query_info["target_type"]+":"+target_node_name

            mg.add_node(target_node_id, name=target_node_name, type=query_info["target_type"], url=target_node_url)

            if query_info["target_type"] == "Person":
               mg.nodes[target_node_id]['icon_url'] = get_person_icon_url_prefetched(target_node_name)

            edge_id = edge_type + ":" + source_node_id + ":" + target_node_id
            r_edge_id = query_info["reverse_direction"] + ":" + target_node_id + ":" + source_node_id

            if query_info["do_reverse"]: # and edge_id not in mg.edges() and r_edge_id not in mg.edges():
              mg.add_edge(target_node_id, source_node_id, id=r_edge_id, key=query_info["reverse_direction"], type=query_info["reverse_direction"], name=query_info["plain_text"])

            if not query_info["do_reverse"]:# and edge_id not in mg.edges() and r_edge_id not in mg.edges():
              mg.add_edge(source_node_id, target_node_id, id=edge_id, key=edge_type, type=edge_type, name=query_info["plain_text"])


    print(f"Network size of {mg.number_of_nodes()} nodes and {mg.number_of_edges()} edges")
  with open("wpu-network.pkl", "wb") as file:
    print("Saving")
    pickle.dump(mg, file)
  print(c)
  return mg


def populate_cache():
  mg = get_wpu_connectome_nx()
  nx1 = nx.classes.graphviews.subgraph_view(mg, filter_node=lambda n: False, filter_edge=lambda n1, n2: False)

  with open("wpu-network-nx.pkl", "wb") as file:
       print("Saving")
       pickle.dump(nx1, file)
  d = get_wpu_connectome_dash()

if __name__=="__main__":
  populate_cache()
