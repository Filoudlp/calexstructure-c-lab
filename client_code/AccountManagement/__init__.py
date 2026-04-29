from ._anvil_designer import AccountManagementTemplate
from anvil import *
from routing import router
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .ChangeName import ChangeName
from .ChangeEmail import ChangeEmail
from .DeleteAccountAlert import DeleteAccountAlert

from routing.router import navigate

class AccountManagement(AccountManagementTemplate):
  def __init__(self, **properties):
    self.user = anvil.users.get_user()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    val = anvil.server.call('is_user_subscribed')
    if val:
      txt = "Abonnement : C-Lab"
    else:
      txt = "Abonnement : Free"
    self.lbl_abo.text = txt
    # Any code you write here will run before the form opens

  def change_name_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    new_name = alert(ChangeName(item=self.user["name"]), title="Change name", buttons=None, dismissible=True, large=True)
    if new_name:
      self.user = anvil.server.call('change_name', new_name)
      self.refresh_data_bindings()

  def change_email_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    new_email = alert(ChangeEmail(item=self.user["email"]), title="Change email", buttons=None, dismissible=True, large=True)
    if new_email:
      self.user = anvil.server.call('change_email', new_email)
      self.refresh_data_bindings()

  def reset_password_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    if confirm("Resetting your password will send a reset email to your inbox and log you out. Do you want to continue?"):
      anvil.users.send_password_reset_email(self.user["email"])
      alert("A password reset email has been sent to your inbox.", title="Password reset email sent")
      anvil.users.logout()
      navigate(path="/")

  def delete_account_link_click(self, **event_args):
    """This method is called when the button is clicked"""
    if alert(DeleteAccountAlert(), buttons=None, large=True):
      anvil.server.call('delete_user')
      anvil.users.logout()
      navigate(path="/")
