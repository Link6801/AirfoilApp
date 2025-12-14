import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="NACA 4-Digit Airfoil Generator", layout="wide")
st.sidebar.header("Airfoil Parameters")
with st.sidebar:
    choice = st.selectbox( "Choose an Airfoil Family",["NACA 4-Digit Series","NACA 5-Digit Series"],index=0)
    if choice=="NACA 4-Digit Series":
        sp = st.sidebar.slider("Cosine Spacing", 50, 70, 60 ,1)
        st.sidebar.caption("*Warning: 60 is the sweet spot, higher values may cause artifacting in XLFR5*")
        m = st.sidebar.slider("Maximum Camber (m)", 0.00, 0.09, 0.02, 0.01)
        p = st.sidebar.slider("Position of Max Camber (p)", 0.0, 0.9, 0.4, 0.1)
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
        st.sidebar.markdown("Work in Progress")
        
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