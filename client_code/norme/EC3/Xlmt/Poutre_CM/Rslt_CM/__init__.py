from ._anvil_designer import Rslt_CMTemplate
from routing import router
import stripe.checkout
import m3.components as m3
from anvil import handle

class Rslt_CM(Rslt_CMTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
