import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

st.set_page_config(page_title="FoilLabs - Geometry Simplified", page_icon="✈️",layout="wide")
st.sidebar.header("Airfoil Parameters")
with st.sidebar:
    choice = st.selectbox( "Choose an Airfoil Family",["NACA 4-Digit Series","NACA 5-Digit Series"],index=0)
    if choice=="NACA 4-Digit Series":
        sp = st.sidebar.slider("Cosine Spacing", 50, 70, 60 ,1)
        st.sidebar.caption("*Warning: 60 is the sweet spot, higher values may cause artifacting in XLFR5*")
        m = st.sidebar.slider("Maximum Camber (m)", 0.00, 0.09, 0.02, 0.01)
        p = st.sidebar.slider("Position of Max Camber (p)", 0.1, 0.9, 0.4, 0.1)
        t = st.sidebar.slider("Maximum Thickness (t)", 0.01, 0.3, 0.12, 0.01)
        if t>=0.10:
            naca = f"NACA {int(m*100)}{int(p*10)}{int(t*100)}"
        else:
            naca = f"NACA {int(m*100)}{int(p*10)}0{int(t*100)}"
        st.sidebar.write(f"**Selected Airfoil:** {naca}")
        x = 0.5 * (1 - np.cos(np.linspace(0, np.pi, sp)))
        z = (t/0.2)*(0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1015*x**4)

        yc = np.where(x < p,
                    m/p**2*(2*p*x - x**2),
                    m/(1-p)**2*((1-2*p)+2*p*x - x**2))
        dyc_dx = np.where(x < p,
                        2*m/p**2*(p - x),
                        2*m/(1-p)**2*(p - x))
        theta = np.arctan(dyc_dx)

        xu = x - z*np.sin(theta)
        yu = yc + z*np.cos(theta)
        xl = x + z*np.sin(theta)
        yl = yc - z*np.cos(theta)

    elif choice=="NACA 5-Digit Series":
        sp = st.sidebar.slider("Cosine Spacing", 50, 70, 60 ,1)
        st.sidebar.caption("*Warning: 60 is the sweet spot, higher values may cause artifacting in XLFR5*")
        l = st.sidebar.slider("Lift Coefficient (m)", 0.15, 1.35, 0.30, 0.15)
        p = st.sidebar.slider("Position of Max Camber (p)", 0.05, 0.40, 0.10, 0.05)
        col1, col2 = st.columns([4,1],vertical_alignment="center")
        with col1:
            st.write("Reflex Camber?")
        with col2:
            ref = st.toggle(label="reflex", label_visibility="collapsed")
        reflex=0
        if ref:
            reflex=1
        else:
            reflex=0
        t = st.sidebar.slider("Maximum Thickness (t)", 0.01, 0.3, 0.12, 0.01)
        if t>=0.10:
            naca = f"NACA {int(l/0.15)}{int(p*20)}{reflex}{int(t*100)}"
        else:
            naca = f"NACA {int(l/0.15)}{int(p*20)}{reflex}0{int(t*100)}"
        st.sidebar.write(f"**Selected Airfoil:** {naca}")
        if reflex==0:
            def F(r):
                return r*(1-(r/3)**0.5)-p
            r1,r2,r=brentq(F,0,4/3,xtol=1e-12, rtol=1e-12, maxiter=1000),brentq(F,4/3,3,xtol=1e-12, rtol=1e-12, maxiter=1000),0
            if r1>1:
                r=r2
            else:
                r=r1
            N=(3*r - 7*r**2 + 8*r**3 - 4*r**4) / np.sqrt(r * (1 - r))- (3/2) * (1 - 2*r) * (np.pi/2 - np.arcsin(1 - 2*r))
            k1=(6*(0.15*int(l/0.15)))/N
            x = 0.5 * (1 - np.cos(np.linspace(0, np.pi, sp)))
            z = (t/0.2)*(0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1015*x**4)

            yc=np.where(x<r,
                        (k1 / 6) * (x**3 - 3*r*x**2 + r**2*(3 - r)*x),
                        (k1 * r**3 / 6) * (1 - x))
            dyc_dx=np.where(x<r,
                            (k1 / 6) * (3*x**2 - 6*r*x + r**2*(3 - r)),
                            - (k1 * r**3) / 6)
            theta = np.arctan(dyc_dx)

            xu = x - z*np.sin(theta)
            yu = yc + z*np.cos(theta)
            xl = x + z*np.sin(theta)
            yl = yc - z*np.cos(theta)

        elif reflex==1:
            print()

        st.sidebar.markdown("Work in Progress")
        
try:
    n=choice.split("Series")
    st.title(n[0]+"Airfoil Visualizer")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(xu, yu, 'b', label='Upper Surface')
    ax.plot(xl, yl, 'r', label='Lower Surface')
    ax.plot(x, yc, 'k--', label='Mean Camber Line')

    ax.axis('equal')
    ax.set_xlabel("x / Chord")
    ax.set_ylabel("y / Chord")
    ax.set_title(naca)
    ax.legend()
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

    X = np.concatenate([xu[::-1], xl[1:]])
    Y = np.concatenate([yu[::-1], yl[1:]])

    dat_text = f"{naca} Airfoil"
    for xi, yi in zip(X, Y):
        dat_text += f"\n  {xi:.6f} {yi:.6f}"
            
    st.download_button(
    label="Download .dat file",
    data=dat_text,
    file_name=f"{naca}.dat",
    mime="text/plain")
except Exception as e:
    st.markdown(e)
    st.markdown(f"{choice} is under construction, you patience is appreciated.")