from ._anvil_designer import option_avancer_CMTemplate
from routing import router
import stripe.checkout
from anvil import handle

class option_avancer_CM(option_avancer_CMTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
