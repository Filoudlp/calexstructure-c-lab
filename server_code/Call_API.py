import anvil.stripe
import anvil.server
import anvil.http
import json

# URL de ton API hébergée sur ton serveur (ou Uplink)
API_BASE_URL = "https://alex25071.pythonanywhere.com"
API_KEY = 1#anvil.secrets.get_secret("my_api_key") # Pour sécuriser l'accès

@anvil.server.callable
def api_call(api_url, payload_json):
  """
    Reçoit le JSON préparé par le client, l'envoie à l'API externe,
    et renvoie le JSON de résultat.
    """
  url = f"{API_BASE_URL}{api_url}"

  headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY # Authentification
  }

  try:
    # Envoi de la requête POST
    response = anvil.http.request(
      url=api_url,
      method="POST",
      data=payload_json,
      headers=headers,
      json=True # Anvil convertit automatiquement le JSON en dictionnaire Python
    )
    try:
      response = anvil.http.request(
        url=API_URL,
        method="POST",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        json=True,  # parse automatiquement la réponse JSON
      )
    # La réponse est déjà un dictionnaire Python grâce à json=True
    return response

  except anvil.http.HttpError as e:
    # Gestion des erreurs HTTP (400, 500, etc.)
    return {"error": f"Erreur API ({e.status}): {e.content}"}
  except Exception as e:
    return {"error": f"Erreur inattendue : {str(e)}"}