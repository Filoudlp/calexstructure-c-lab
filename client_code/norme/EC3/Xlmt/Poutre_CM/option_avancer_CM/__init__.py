from ._anvil_designer import option_avancer_CMTemplate
import stripe.checkout
import m3.components as m3
from anvil import handle

class option_avancer_CM(option_avancer_CMTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
