from routing import router
import anvil.server
from anvil import *
import json

from collections import namedtuple

# This is a package.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Package1
#
#    Package1.say_hello()
#

#@anvil.server.route("/hello")
#def poutre_cm(**p):
#  open_form('norme.EC3.Xlmt.Poutre_CM') 

def check_connectednsub(var):
  if not anvil.users.get_user():
    print("not connected")
    user = anvil.users.login_with_form(allow_cancel=True, show_signup_option=True,
                                       allow_remembered=True, remember_by_default=False)
    if user:
      open_form(var)
      print("succeed")
    else:
      open_form('Landing_LoginPage')

  user = anvil.users.get_user()
  if user["subscription"] != "Abonnement C-Lab":
    print('bien ouej mon reuf')
  else:
    print("no subscription")

def api_call(api_url, payload_json=None):
  """
    Reçoit le JSON préparé par le client, l'envoie à l'API externe,
    et renvoie le JSON de résultat.
  """
  API_BASE_URL = "https://alex25071.pythonanywhere.com"
  STR_LIB_KEY = "yl/CHoKfdeUg0PquMpboBw==" #anvil.secrets.get_secret('str_lib_api_secret_key')
  url = f"{API_BASE_URL}{api_url}"
  headers = {
    "Content-Type": "application/json",
    "X-API-KEY": STR_LIB_KEY # Authentification
  }
  if payload_json is None:
    try:
      response = anvil.http.request(
        url=url,
        method="POST",
        headers=headers,
        json=True,  # parse automatiquement la réponse JSON
      )
      # La réponse est déjà un dictionnaire Python grâce à json=True
      return response

    except anvil.http.HttpError as e:
      # Gestion des erreurs HTTP (400, 500, etc.)
      return {"error": f"Erreur API ({e.status}): {e.content}"}
    except Exception as e:
      return {"error": f"Erreur inattendue : {str(e)}"}
  else:
    try:
      response = anvil.http.request(
        url=url,
        method="POST",
        data=json.dumps(payload_json),
        headers=headers,
        json=True,  # parse automatiquement la réponse JSON
      )
      # La réponse est déjà un dictionnaire Python grâce à json=True
      return response
  
    except anvil.http.HttpError as e:
      # Gestion des erreurs HTTP (400, 500, etc.)
      return {"error": f"Erreur API ({e.status}): {e.content}"}
    except Exception as e:
      return {"error": f"Erreur inattendue : {str(e)}"}

def convert_unit(val: float, base: str, end: str):
  """ Fonction to convert unit with category check """
  # Définition des familles d'unités
  g = 9.81
  categories = {
    "force_masse": {
      "n": 1, "dn": 10, "kn": 1000, "mn": 1000000,
      "g": 0.001 * g, "kg": 1 * g, "t": 1000 * g 
    },
    "longueur": {
      "m": 1, "dm": 0.1, "cm": 0.01, "mm": 0.001, "km": 1000
    },
    "pression": {
      "pa": 1, "kpa": 1000, "mpa": 1000000, "bar": 100000
    }
  }

  base, end = base.lower(), end.lower()

  # Trouver à quelle catégorie appartient l'unité de base
  for units in categories.values():
    if base in units and end in units:
      return val * (units[base] / units[end])

    # Si on arrive ici, c'est que les unités sont incompatibles ou inconnues
  raise ValueError(f"Conversion impossible entre '{base}' et '{end}'.")

#==========
#= Var CM =
#==========

# ---------------------------------------------------------------------
# Définition de la structure Variable
# ---------------------------------------------------------------------
Variable = namedtuple("Variable", ["name", "value", "unit", "formula", "ref"])

# ---------------------------------------------------------------------
# Registre central des variables
# ---------------------------------------------------------------------
_INPUT_REGISTRY = {
  v.name: v for v in [
    # --- Sollicitations ---
    Variable("Ned", "10", "kN",   "Effort normal de calcul",      "EC3 §6.2.4"),
    Variable("Med", "10", "kN.m", "Moment fléchissant de calcul", "EC3 §6.2.5"),
    Variable("Ved", "10", "kN",   "Effort tranchant de calcul",   "EC3 §6.2.6"),

    # --- Matériau ---
    Variable("fy", "235", "MPa",  "Limite élastique",             "EC3 §3.2"),
    Variable("fu",  "235", "MPa",  "Résistance ultime",            "EC3 §3.2"),

    # --- Section ---
    Variable("b",  "200",   "mm", "Base de la section",          "—"),
    Variable("h", "500",    "mm", "Hauteur de la section",          "—"),
    Variable("e",  "10",   "mm", "Epaisseur de la section",          "—"),
    Variable("A",   "1000",  "mm²", "Aire de la section",          "—"),
    Variable("Anet", "1000", "mm²", "Aire nette de la section",    "—"),
    Variable("Av",  "1000",   "mm²", "Aire de cisaillement de la section",          "—"),
    Variable("Iy",  "10000",   "mm4", "Inertie axe Y de la section",          "—"),
    Variable("Iz",  "10000",   "mm4", "Inertie axe Z de la section",          "—"),
    Variable("Wy",  "10000",   "mm3", "Module élastique axe Y de la section",          "—"),
    Variable("Wz",  "10000",   "mm3", "Module élastique axe Z de la section",          "—"),

    # --- Coefficients partiels ---
    Variable("γm0", "1.0", "-", "Coefficient partiel γM0",    "EC3 §6.1"),
    Variable("γm1", "1.0", "-", "Coefficient partiel γM1",    "EC3 §6.1"),
    Variable("γm2", "1.0", "-", "Coefficient partiel γM2",    "EC3 §6.1"),

    Variable("γc", "1.5", "-", "Coefficient partiel γc",    "EC2 §2.4.2.4"),
    Variable("γc", "1.15", "-", "Coefficient partiel γs",    "EC2 §2.4.2.4"),
  ]
}


def get_rowitem_input(name: str):
  """
    Retourne la définition d'une variable d'entrée à partir de son nom.

    :param name: Nom de la variable (ex. "Ned", "fy", "A").
    :return:     Objet Variable correspondant.
    :raises TypeError: si name n'est pas une str.
    :raises KeyError:  si la variable n'est pas répertoriée.
    """
  if not isinstance(name, str):
    raise TypeError(f"Le nom de la variable doit être une str, reçu {type(name).__name__}.")

  key = name.strip()
  var = _INPUT_REGISTRY.get(key)

  if var is None:
    # Recherche insensible à la casse en secours
    for k, v in _INPUT_REGISTRY.items():
      if k.lower() == key.lower():
        return v
    raise KeyError(f"Variable inconnue : '{name}'. "
                   f"Variables disponibles : {list(_INPUT_REGISTRY.keys())}")
  return var