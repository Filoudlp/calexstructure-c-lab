from ._anvil_designer import RowPlotTemplate
from anvil import *

from plotly import graph_objs as go

class RowPlot(RowPlotTemplate):
  def __init__(self, val, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Valeur à afficher
    pourcentage = val * 100

    # Couleur conditionnelle
    couleur = 'green' if pourcentage < 100 else 'red'

    # Gérer le cas > 100% (on plafonne visuellement à 100)
    valeur_affichee = min(pourcentage, 100)
    reste = 100 - valeur_affichee

    fig = go.Figure(data=[go.Pie(
      values=[valeur_affichee, reste],
      labels=['Atteint', 'Restant'],
      hole=0.6,
      marker=dict(colors=[couleur, '#E8E8E8']),
      textinfo='none',            # Pas de texte sur les parts
      hoverinfo='skip',           # Pas de survol
      sort=False,                 # Garde l'ordre
      direction='clockwise',
      rotation=0,
      showlegend=False
    )])

    fig.update_layout(
      annotations=[
        dict(
          text=f'<b>{pourcentage:.2f}%</b>',
          x=0.5, y=-0.10,
          xref='paper', yref='paper',
          font=dict(size=14, color=couleur),
          showarrow=False
        ),
      ],
      margin=dict(t=20, b=40, l=20, r=20),
    )
    self.plt.figure = fig
