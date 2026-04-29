import anvil.stripe
import anvil.server
import anvil.http
import anvil.secrets
import json

# URL de ton API hébergée sur ton serveur (ou Uplink)
API_BASE_URL = "https://alex25071.pythonanywhere.com"
STR_LIB_KEY = anvil.secrets.get_secret('str_lib_api_secret_key')

@anvil.server.callable
def api_call(api_url, payload_json=None):
  """
    Reçoit le JSON préparé par le client, l'envoie à l'API externe,
    et renvoie le JSON de résultat.
  """
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
        #json=True,  # parse automatiquement la réponse JSON
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