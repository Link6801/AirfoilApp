import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

st.set_page_config(page_title="NACA 4-Digit Airfoil Generator", layout="wide")

st.title("NACA 4-Digit Airfoil Visualizer")

st.sidebar.header("Airfoil Parameters")
smooth = st.sidebar.checkbox("Enable spline smoothing", value=False)
m = st.sidebar.slider("Maximum Camber (m)", 0.00, 0.09, 0.02, 0.01)
p = st.sidebar.slider("Position of Max Camber (p)", 0.0, 0.9, 0.4, 0.1)
t = st.sidebar.slider("Maximum Thickness (t)", 0.01, 0.3, 0.12, 0.01)
if t>=0.10:
    naca = f"NACA {int(m*100)}{int(p*10)}{int(t*100)}"
else:
    naca = f"NACA {int(m*100)}{int(p*10)}0{int(t*100)}"
st.sidebar.write(f"**Selected Airfoil:** {naca}")
x = 0.5 * (1 - np.cos(np.linspace(0, np.pi, 200)))
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

fig, ax = plt.subplots(figsize=(10, 4))
if smooth==True:
    spline_xu = UnivariateSpline(np.arange(len(xu)), xu, s=1e-6)
    spline_yu = UnivariateSpline(np.arange(len(yu)), yu, s=1e-6)
    spline_xl = UnivariateSpline(np.arange(len(xl)), xl, s=1e-6)
    spline_yl = UnivariateSpline(np.arange(len(yl)), yl, s=1e-6)

    ux=spline_xu(np.arange(len(xu)))
    uy=spline_yu(np.arange(len(yu)))
    lx=spline_xl(np.arange(len(xl)))
    ly=spline_yl(np.arange(len(yl)))

else:
    ux,uy,lx,ly=xu,yu,xl,yl

ax.plot(ux, uy, 'b', label='Upper Surface')
ax.plot(lx, ly, 'r', label='Lower Surface')
ax.plot(x, yc, 'k--', label='Mean Camber Line')

ax.axis('equal')
ax.set_xlabel("x / Chord")
ax.set_ylabel("y / Chord")
ax.set_title(naca)
ax.legend()
ax.grid(True, alpha=0.3)
if smooth==True:
    ax.text(0.05, 0.95, "Smoothing: ON", transform=ax.transAxes,
            fontsize=10, color="green", verticalalignment="top")
else:
    ax.text(0.05, 0.95, "Smoothing: OFF", transform=ax.transAxes,
            fontsize=10, color="red", verticalalignment="top")


st.pyplot(fig)

X = np.concatenate([ux[::-1], lx[1:]])
Y = np.concatenate([uy[::-1], ly[1:]])

dat_string = f"{naca}\n"
for xi, yi in zip(X, Y):
    dat_string += f"{xi:.6f}  {yi:.6f}\n"

st.download_button(
    label="Download .dat Airfoil File",
    data=dat_string.encode("ascii", "ignore"),
    file_name=f"{naca}.dat",
    mime="text/plain"
)
