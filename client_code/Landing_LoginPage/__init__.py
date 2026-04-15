from ._anvil_designer import Landing_LoginPageTemplate
from anvil import *
import stripe.checkout
import m3.components as m3
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Landing_LoginPage(Landing_LoginPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.login_with_form(allow_cancel=True, show_signup_option=True,
                                       allow_remembered=True, remember_by_default=False)
    if user:
      open_form('norme.EC3.Xlmt.Poutre_CM')

  # TODO check if this works in init, move if it does
  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    pass
    #if anvil.users.get_user():
     # open_form('norme.EC3.Xlmt.Poutre_CM')