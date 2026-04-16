from routing import router
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import json

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