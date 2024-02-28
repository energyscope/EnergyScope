import numpy as np
import plotly.graph_objects as go

# Définir la fonction avec une décroissance exponentielle vers 0
def exp_decroissante(x):
    return (1- np.exp(-(2050 - x)/5))*60

# Définir la fonction avec une décroissance exponentielle inverse vers 0
def exp_decroissante_inverse(x):
    return 60*np.exp(-(x - 2023)/5)

# Générer des valeurs x
x_values = np.linspace(2023, 2050, 100)

# Calculer les valeurs y pour chaque fonction
y_exp = exp_decroissante(x_values)
y_inv_exp = exp_decroissante_inverse(x_values)

# Créer une figure Plotly
fig = go.Figure()

# Tracer les deux fonctions
fig.add_trace(go.Scatter(x=x_values, y=y_exp, mode='lines', line=dict(width=7)))#, name='Décroissance exponentielle'))
fig.add_trace(go.Scatter(x=x_values, y=y_inv_exp, mode='lines', line=dict(width=7)))#, name='Décroissance exponentielle inverse'))

# Remplir la partie hachurée entre les courbes
fig.add_trace(go.Scatter(
    x=np.concatenate((x_values, x_values[::-1])),
    y=np.concatenate((y_exp, y_inv_exp[::-1])),
    fill='toself',
    fillcolor='rgba(0,100,80,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    name='Zone hachurée'
))
# Ajouter des titres et des étiquettes d'axes
fig.update_layout(
    title='Tracé de fonctions avec zone hachurée (2023-2050)',
    xaxis_title='Year',
    yaxis_title='Emissions',
)

# Afficher la figure
fig.show()
