from ._anvil_designer import HomepageLayoutTemplate
from anvil import *


class HomepageLayout(HomepageLayoutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
