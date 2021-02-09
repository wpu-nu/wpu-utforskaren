import dash

import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

def bp():
  from pudb import set_trace; set_trace()

from bot_pass import *
# Create bot-passwords for your wpu user and
# create bot_pass.py like this
# wpu_username="Botten Anna@OCRBOT"
# wpu_password="password"

queries = {
  "Person": {
    "query": f"[[Kategori:Person]] | ?=Person",
    "source_type": "Person"
  },
  "Section": {
    "query": f"[[Kategori:Uppslag]] | ?=Section",
    "source_type": "Section"
  },
  "Section_Mentioned_Person": {
    "query": f"[[Har NämndaPersoner::+]] |?Har NämndaPersoner=Section_Mentioned_Person",
    "source_type": "Section",
    "target_type": "Person",
    "do_reverse": False,
    "reverse_direction": "Person_MentionedIn_Section",
    "plain_text": "Omnämnd i"
  },
  "Person_MentionedIn_Section": {
    "query": f"[[-Har NämndaPersoner::+]]|?-Har NämndaPersoner=Person_MentionedIn_Section",
    "source_type": "Person",
    "target_type": "Section",
    "do_reverse": True,
    "reverse_direction": "Section_Mentioned_Person",
    "plain_text": "Omnämnd i"
  },
  "Section_WasInterrogationOf_Person": {
    "query": f"[[Har Uppgiftslämnare::+]] |?Har Uppgiftslämnare=Section_WasInterrogationOf_Person",
    "source_type": "Section",
    "target_type": "Person",
    "do_reverse": True,
    "reverse_direction": "Person_WasInterrogatedIn_Section",
    "plain_text": "Förhör av"
  },
  "Person_WasInterrogatedIn_Section": {
    "query": f"[[-Har Uppgiftslämnare::+]]|?-Har Uppgiftslämnare=Person_WasInterrogatedIn_Section ",
    "source_type": "Person",
    "target_type": "Section",
    "do_reverse": False,
    "reverse_direction": "Section_WasInterrogationOf_Person",
    "plain_text": "Förhör av"
  },
  "Section_WasInterrogationBy_Person": {
    "query": f"[[Har Uppgiftsmottagare::+]] |?Har Uppgiftsmottagare=Section_WasInterrogationBy_Person",
    "source_type": "Section",
    "target_type": "Person",
    "do_reverse": False,
    "reverse_direction": "Person_WasInterrogatorIn_Section",
    "plain_text": "Förhörsledare"
  },
  "Person_WasInterrogatorIn_Section": {
    "query": f"[[-Har Uppgiftsmottagare::+]]|?-Har Uppgiftsmottagare=Person_WasInterrogatorIn_Section",
    "source_type": "Person",
    "target_type": "Section",
    "do_reverse": True,
    "reverse_direction": "Section_WasInterrogationBy_Person",
    "plain_text": "Förhörsledare"
  },
  "Person_Knows_Person": {
    "query": f"[[-foaf:knows::+]]|?-foaf:knows=Person_Knows_Person ",
    "source_type": "Person",
    "target_type": "Person",
    "do_reverse": False,
    "reverse_direction": "Person_Knows_Person_reversed",
    "plain_text": "Känner"
  },
  "Person_Knows_Person_reversed": {
    "query": f"[[foaf:knows::+]]|?Foaf:knows=Person_Knows_Person ",
    "source_type": "Person",
    "target_type": "Person",
    "do_reverse": True,
    "reverse_direction": "Person_Knows_Person",
    "plain_text": "Känner"
  },
  "Section_RelatesTo_Section": {
    "query": f"[[Har Anknytningar::+]] |?=Section |?Har Anknytningar=Section_RelatesTo_Section",
    "source_type": "Section",
    "target_type": "Section",
    "do_reverse": False,
    "reverse_direction": "Section_RelatesTo_Section_reversed",
    "plain_text": "Anknyter"
  },
  "Section_RelatesTo_Section_reversed": {
    "query": f"[[-Har Anknytningar::+]] |?-Har Anknytningar=Section_RelatesTo_Section",
    "source_type": "Section",
    "target_type": "Section",
    "do_reverse": True,
    "reverse_direction": "Section_RelatesTo_Section",
    "plain_text": "Anknyter"
  }
}

cyto.load_extra_layouts()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
from flask_caching import Cache
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})
