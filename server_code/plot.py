import anvil.stripe
import anvil.server
import anvil.mpl_util
import numpy as np
import matplotlib.pyplot as plt

@anvil.server.callable
def make_plot():
  # Données
  sizes = [40, 25, 20, 10, 5]
  labels = ['Python', 'JavaScript', 'C++', 'Java', 'Autres']
  colors = plt.cm.viridis([0.1, 0.3, 0.5, 0.7, 0.9])
  explode = [0.1 if s == max(sizes) else 0 for s in sizes]
  
  # Tracé
  plt.figure(figsize=(7,7))
  wedges, texts, autotexts = plt.pie(
    sizes,
    labels=labels,
    autopct=lambda p: f'{p:.1f}%\n({int(p*sum(sizes)/100)})',
    colors=colors,
    explode=explode,
    startangle=140,
    textprops={'color':"w", 'fontsize':12},
    shadow=True
  )
  
  plt.setp(autotexts, size=10, weight="bold")
  plt.title("Popularité des langages de programmation", fontsize=14)

  # Return this plot as a PNG image in a Media object
  return anvil.mpl_util.plot_image()