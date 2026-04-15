from ._anvil_designer import frmTemplate
from anvil import *
from routing import router
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from anvil.js import get_dom_node


class frm(frmTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    dom = get_dom_node(self)

    # Brancher le bouton Calculer
    btn = dom.querySelector('.btn-calculer')
    if btn:
      btn.addEventListener('click', self.lancer_calcul)

      # Brancher le toggle options avancées
    cb = dom.querySelector('input[anvil-name="cb_options_avancees"]')
    if cb:
      cb.addEventListener('change', self.toggle_options_avancees)

    # ─────────────────────────────────────────────
    # UTILITAIRES LECTURE / ÉCRITURE
    # ─────────────────────────────────────────────
  def lire_valeur(self, dom, anvil_name, defaut=0.0):
    el = dom.querySelector(f'input[anvil-name="{anvil_name}"]')
    if el and el.value:
      try:
        return float(el.value)
      except ValueError:
        return defaut
    return defaut

  def lire_select(self, dom, anvil_name, defaut=""):
    el = dom.querySelector(f'select[anvil-name="{anvil_name}"]')
    if el and el.value:
      return el.value
    return defaut

    # ─────────────────────────────────────────────
    # TOGGLE OPTIONS AVANCÉES
    # ─────────────────────────────────────────────
  def toggle_options_avancees(self, event):
    dom = get_dom_node(self)
    bloc = dom.querySelector('.advanced-options')
    if bloc:
      cb = dom.querySelector('input[anvil-name="cb_options_avancees"]')
      if cb and cb.checked:
        bloc.style.display = 'block'
      else:
        bloc.style.display = 'none'

    # ─────────────────────────────────────────────
    # CALCUL PRINCIPAL
    # ─────────────────────────────────────────────
  def lancer_calcul(self, event):
    dom = get_dom_node(self)

    # --- Lecture entrées (calées sur tes anvil-name) ---
    section_type = self.lire_select(dom, "dd_section", "Rectangulaire")
    b = self.lire_valeur(dom, "tb_largeur_b", 30.0)
    h = self.lire_valeur(dom, "tb_hauteur_h", 50.0)
    fyk = self.lire_valeur(dom, "tb_fyk", 500.0)
    ned = self.lire_valeur(dom, "tb_ned", 1000.0)

    # Options avancées
    es = self.lire_valeur(dom, "tb_es", 200000.0)
    nuance = self.lire_select(dom, "dd_nuance", "B")
    eud = self.lire_valeur(dom, "tb_eud", 0.01)
    gamma_s = self.lire_valeur(dom, "tb_gamma_s", 1.15)

    # --- Vérification ---
    if b <= 0 or h <= 0:
      alert("Erreur : largeur et hauteur doivent être > 0")
      return

      # --- Appel serveur ---
    try:
      donnees = {
        'section_type': section_type,
        'b': b,
        'h': h,
        'fyk': fyk,
        'ned': ned,
        'es': es,
        'nuance': nuance,
        'eud': eud,
        'gamma_s': gamma_s
      }

      result = anvil.server.call('calculer_section', donnees)

      # --- Affichage résultat simple (alert pour l'instant) ---
      msg = ""
      for cle, valeur in result.items():
        msg += f"{cle} : {valeur}\n"
      alert(msg)

    except Exception as e:
      alert(f"Erreur : {str(e)}")
