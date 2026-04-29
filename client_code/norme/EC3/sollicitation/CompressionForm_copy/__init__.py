from ._anvil_designer import CompressionForm_copyTemplate
from anvil import *
from routing import router
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil.js import get_dom_node

from ..BlockCard import BlockCard
from ..RowItem import RowItem


class CompressionForm_copy(CompressionForm_copyTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Container flex pour aligner les 4 cards côte à côte
    container = self.flow_panel_1
    #self.flow_panel_1.add_component(container)

    # Active flexbox pour largeurs égales
    node = get_dom_node(container)
    node.style.display = "flex"
    node.style.gap = "10px"
    node.style.alignItems = "flex-start"

    # ============== 4 BlockCards ==============
    cards_data = [
      ("Compression",     "#FFF2CC"),
      ("Traction",        "blue"),
      ("Flexion",         "#E2EFDA"),
      ("Cisaillement",    "#FCE4D6"),
    ]

    for title, color in cards_data:
      card = BlockCard(title=title, header_color=color)
      container.add_component(card)
      #get_dom_node(card).style.flex = "1"

      # Ajoute du contenu dans chaque card
      card.add_input(RowItem(
        name="Ned", value=500, unit="kN",
        formula="Effort", ref="EC3",
        editable=True, row_type="input"
      ))
      card.add_input(RowItem(
        name="Nrd", value="1264", unit="kN",
        formula="A·fy/γM0", ref="§6.2.4",
        editable=False, row_type="result"
      ))