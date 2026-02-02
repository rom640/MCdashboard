'''
from tkinter import *
from PIL import Image, ImageTk
import numpy
matlib
'''
"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Exemple de données
x = [1, 2, 3, 4, 5]
y = [10, 5, 8, 12, 7]

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Mon graphique")

# Création du graphique avec matplotlib
fig, ax = plt.subplots()
ax.plot(x, y)

# Intégration dans Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

root.mainloop()
"""
"""
from flask import Flask, render_template_string
import random

app = Flask(__name__)

@app.route("/")
def index():
    data = [random.randint(0, 10) for _ in range(5)]
    html = f"<h1>Mes données bla bla bla : {data}</h1>"
    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True)
"""

"""
import streamlit as st
import pandas as pd
import numpy as np

# Tes données : exemple avec DataFrame
df = pd.DataFrame({
    "Nom": ["A", "B", "C"],
    "Valeur": [10, 5, 8]
})

st.title("Mon mini dashboard")
st.write("Voici mes données :")
st.dataframe(df)

# Graphique simple
st.bar_chart(df.set_index("Nom"))
"""