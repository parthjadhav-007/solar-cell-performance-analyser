## Solar Cell Performance Analyser

A command-line Python program that estimates solar cell performance with a simple single-diode model, then plots current-voltage and power-voltage curves.

### Features

- Estimate the maximum power point, fill factor, efficiency, and load resistance.
- Analyse changes in light intensity and cell temperature.
- Plot I-V and P-V curves for the entered operating conditions and comparison cases.

### Requirements

- Python 3
- NumPy
- Matplotlib

Install the libraries with:

```bash
python -m pip install numpy matplotlib
```

### Run

```bash
python solar_cell_analyser.py
```

Enter the cell measurements, cell area, light intensity, and temperature when prompted. The program prints the calculated performance values and opens the plots in Matplotlib windows.
