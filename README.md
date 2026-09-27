# FoilLabs — Geometry Simplified

A lightweight Python/Streamlit application for generating, visualizing, and exporting **NACA airfoil geometries**.

FoilLabs was built as an engineering-oriented tool to make airfoil geometry generation easier to experiment with, visualize, and use in further aerodynamic workflows.

## 🌐 Live Demo

**Try FoilLabs here:**

https://airfoilapp-9o4m7lcu48b6zjffan6ixf.streamlit.app/

---

## ✈️ Features

### NACA 4-Digit Airfoils

Generate NACA 4-digit airfoils by specifying:

- Maximum camber
- Position of maximum camber
- Maximum thickness
- Coordinate resolution
- Cosine spacing

### NACA 5-Digit Airfoils

Generate NACA 5-digit airfoil geometries and explore their camber-line characteristics.

> **🚧 Development Note:** Reflexed camber-line profiles for the NACA 5-digit series are currently **under development** and are not yet fully supported.

### 📈 Geometry Visualization

Visualize the generated airfoil geometry directly within the application.

### 📐 Adjustable Cosine Spacing

FoilLabs provides adjustable cosine spacing to control the distribution of coordinate points along the airfoil.

This allows greater point density around important geometric regions such as the leading and trailing edges.

### 📁 `.dat` Export

Generated airfoil coordinates can be exported in `.dat` format for use with external aerodynamic tools and workflows, including:

- XFLR5
- XFOIL
- CAD workflows
- CFD preprocessing

---

## 🧮 How It Works

FoilLabs generates airfoil coordinates mathematically from the selected NACA parameters.

For NACA 4-digit airfoils, the application uses the standard NACA camber-line and thickness-distribution equations to construct the upper and lower surfaces.

The generated coordinates can then be visualized and exported for further analysis.

Cosine spacing can be adjusted to provide a more useful distribution of coordinate points along the airfoil geometry.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **NumPy**
- **Matplotlib**

---

## 🚀 Running Locally

Clone the repository:

```bash
git clone https://github.com/Link6801/AirfoilApp.git
cd AirfoilApp
