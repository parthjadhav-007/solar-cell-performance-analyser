# ============================================================
#  SOLAR CELL PERFORMANCE ANALYSER
#  Basic version: only input(), numpy and matplotlib. No functions.
#
#  Model used (simple single-diode model, series resistance ignored):
#      I = Iph - I0 * (exp(V / (n * Ns * Vt)) - 1)
#  where
#      Iph = light generated current (depends on light intensity)
#      I0  = diode saturation current
#      n   = ideality factor, Ns = number of cells in series
#      Vt  = k*T/q (thermal voltage)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
k = 1.380649e-23      # Boltzmann constant (J/K)
q = 1.602176634e-19   # Charge of an electron (C)

print("=" * 55)
print("        SOLAR CELL PERFORMANCE ANALYSER")
print("=" * 55)
print("Enter the values measured at standard conditions")
print("(1000 W/m2 light and 25 C). Example values are shown.")
print()

# ---------------- INPUTS ----------------
Isc = float(input("Short-circuit current Isc in A (e.g. 0.9): "))
Voc = float(input("Open-circuit voltage Voc in V (e.g. 0.62): "))
n = float(input("Ideality factor, between 1 and 2 (e.g. 1.3): "))
Ns = int(input("Number of cells connected in series (e.g. 1): "))
area = float(input("Total area of the cell in cm2 (e.g. 25): "))
print()
print("Now enter the conditions you want to analyse:")
G = float(input("Light intensity in W/m2 (e.g. 1000): "))
T = float(input("Cell temperature in degree C (e.g. 25): "))

# Simple checks so the program does not crash
if Isc <= 0 or Voc <= 0 or n <= 0 or Ns <= 0 or area <= 0 or G <= 0:
    print("Error: all values must be greater than zero.")
    raise SystemExit

# ---------------- MAIN CALCULATION ----------------
TK = T + 273.15                 # temperature in kelvin
Vt = k * TK / q                 # thermal voltage
a = n * Ns * Vt                 # combined factor used in the equation

# Light increases the current, temperature changes it slightly (+0.05 % per C)
Iph = Isc * (G / 1000) * (1 + 0.0005 * (T - 25))

# Voc falls about 2.3 mV per cell per C, and rises with the log of light
Voc_now = Voc - 0.0023 * Ns * (T - 25) + a * np.log(G / 1000)

if Voc_now <= 0:
    print("Error: at these conditions the open-circuit voltage is zero or less.")
    raise SystemExit

# Find the saturation current so that I = 0 when V = Voc_now
I0 = Iph / (np.exp(Voc_now / a) - 1)

# Voltage from 0 to Voc, then current and power
V = np.linspace(0, Voc_now, 500)
I = Iph - I0 * (np.exp(V / a) - 1)
P = V * I

# Maximum power point (MPP)
index = np.argmax(P)
Vmp = V[index]
Imp = I[index]
Pmax = P[index]

# Other quantities
FF = Pmax / (Voc_now * Iph)             # fill factor
Pin = G * area / 10000                  # input light power in W (cm2 -> m2)
efficiency = Pmax / Pin * 100           # efficiency in %
Rload = Vmp / Imp                       # load resistance at max power

# ---------------- PRINT RESULTS ----------------
print()
print("=" * 55)
print("RESULTS at G = ", G, "W/m2 and T = ", T, "C")
print("=" * 55)
print("Short-circuit current (Isc)   : %.4f A" % Iph)
print("Open-circuit voltage (Voc)    : %.4f V" % Voc_now)
print("Saturation current (I0)       : %.3e A" % I0)
print("Voltage at max power (Vmp)    : %.4f V" % Vmp)
print("Current at max power (Imp)    : %.4f A" % Imp)
print("Maximum power (Pmax)          : %.4f W" % Pmax)
print("Fill factor (FF)              : %.3f" % FF)
print("Input light power             : %.4f W" % Pin)
print("Efficiency                    : %.2f %%" % efficiency)
print("Best load resistance          : %.3f ohm" % Rload)

# ---------------- GRAPH 1: I-V and P-V ----------------
plt.figure("Graph 1 - I-V and P-V curves", figsize=(11, 4.5))

plt.subplot(1, 2, 1)
plt.plot(V, I, color="blue", label="I-V curve")
plt.plot(Vmp, Imp, "ro", label="Max power point")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.title("Current vs Voltage")
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(V, P, color="green", label="P-V curve")
plt.plot(Vmp, Pmax, "ro", label="Max power = %.3f W" % Pmax)
plt.xlabel("Voltage (V)")
plt.ylabel("Power (W)")
plt.title("Power vs Voltage")
plt.grid(True)
plt.legend()

plt.tight_layout()

# ---------------- COMPARISON 1: DIFFERENT LIGHT INTENSITIES ----------------
print()
print("-" * 55)
print("EFFECT OF LIGHT INTENSITY (temperature = %.1f C)" % T)
print("-" * 55)
print("Light (W/m2)   Pmax (W)   Efficiency (%)   FF")

plt.figure("Graph 2 - Effect of light intensity", figsize=(11, 4.5))

for Gx in [200, 400, 600, 800, 1000]:
    Iph_x = Isc * (Gx / 1000) * (1 + 0.0005 * (T - 25))
    Voc_x = Voc - 0.0023 * Ns * (T - 25) + a * np.log(Gx / 1000)
    if Voc_x <= 0:
        continue
    I0_x = Iph_x / (np.exp(Voc_x / a) - 1)
    Vx = np.linspace(0, Voc_x, 300)
    Ix = Iph_x - I0_x * (np.exp(Vx / a) - 1)
    Px = Vx * Ix
    Pmax_x = np.max(Px)
    eff_x = Pmax_x / (Gx * area / 10000) * 100
    FF_x = Pmax_x / (Voc_x * Iph_x)
    print("%8d      %.4f      %.2f            %.3f" % (Gx, Pmax_x, eff_x, FF_x))

    plt.subplot(1, 2, 1)
    plt.plot(Vx, Ix, label="%d W/m2" % Gx)
    plt.subplot(1, 2, 2)
    plt.plot(Vx, Px, label="%d W/m2" % Gx)

plt.subplot(1, 2, 1)
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.title("I-V curves at different light intensities")
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.xlabel("Voltage (V)")
plt.ylabel("Power (W)")
plt.title("P-V curves at different light intensities")
plt.grid(True)
plt.legend()
plt.tight_layout()

# ---------------- COMPARISON 2: DIFFERENT TEMPERATURES ----------------
print()
print("-" * 55)
print("EFFECT OF TEMPERATURE (light = %.0f W/m2)" % G)
print("-" * 55)
print("Temp (C)   Voc (V)   Pmax (W)   Efficiency (%)")

plt.figure("Graph 3 - Effect of temperature", figsize=(11, 4.5))

for Tx in [0, 25, 50, 75]:
    TKx = Tx + 273.15
    a_x = n * Ns * k * TKx / q
    Iph_x = Isc * (G / 1000) * (1 + 0.0005 * (Tx - 25))
    Voc_x = Voc - 0.0023 * Ns * (Tx - 25) + a_x * np.log(G / 1000)
    if Voc_x <= 0:
        continue
    I0_x = Iph_x / (np.exp(Voc_x / a_x) - 1)
    Vx = np.linspace(0, Voc_x, 300)
    Ix = Iph_x - I0_x * (np.exp(Vx / a_x) - 1)
    Px = Vx * Ix
    Pmax_x = np.max(Px)
    eff_x = Pmax_x / Pin * 100
    print("%6d     %.4f    %.4f     %.2f" % (Tx, Voc_x, Pmax_x, eff_x))

    plt.subplot(1, 2, 1)
    plt.plot(Vx, Ix, label="%d C" % Tx)
    plt.subplot(1, 2, 2)
    plt.plot(Vx, Px, label="%d C" % Tx)

plt.subplot(1, 2, 1)
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.title("I-V curves at different temperatures")
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.xlabel("Voltage (V)")
plt.ylabel("Power (W)")
plt.title("P-V curves at different temperatures")
plt.grid(True)
plt.legend()
plt.tight_layout()

print()
print("Close the graph windows to end the program.")
plt.show()
