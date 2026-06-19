import streamlit as st
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

st.title("Problema de producción")

st.subheader("Función objetivo")

gan_folleto = st.number_input(
    "Ganancia por folleto",
    value=25,
    step=1
)

gan_afiche = st.number_input(
    "Ganancia por afiche",
    value=50,
    step=1
)

st.subheader("Restricciones")

hojas_folleto = st.number_input(
    "Hojas por folleto",
    value=4,
    step=1
)

hojas_afiche = st.number_input(
    "Hojas por afiche",
    value=6,
    step=1
)

costo_folleto = st.number_input(
    "Costo por folleto",
    value=15,
    step=1
)

costo_afiche = st.number_input(
    "Costo por afiche",
    value=40,
    step=1
)

max_impresos = st.number_input(
    "Máximo de impresos",
    value=90,
    step=1
)

min_hojas = st.number_input(
    "Mínimo de hojas requeridas",
    value=390,
    step=1
)

max_costo = st.number_input(
    "Costo máximo",
    value=2000,
    step=1
)

variables_enteras = st.checkbox(
    "Resolver con variables enteras",
    value=False
)

if st.button("Resolver"):

    c = [-gan_folleto, -gan_afiche]

    A = [
        [1, 1],
        [hojas_folleto, hojas_afiche],
        [costo_folleto, costo_afiche]
    ]

    bl = [-np.inf, min_hojas, -np.inf]
    bu = [max_impresos, np.inf, max_costo]

    constraints = LinearConstraint(A, bl, bu)

    bounds = Bounds(
        [0, 0],
        [np.inf, np.inf]
    )

    res = milp(
        c=c,
        constraints=constraints,
        bounds=bounds,
        integrality=[1, 1] if variables_enteras else [0, 0]
    )

    if res.success:
        st.success("Problema resuelto")

        st.write(f"Ganancia máxima: {-res.fun:.2f}")
        st.write(f"Folletos: {res.x[0]:.4f}")
        st.write(f"Afiches: {res.x[1]:.4f}")

    else:
        st.error("No se encontró una solución factible.")
