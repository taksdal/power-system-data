import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone
import time

df = pd.read_csv('/Users/olekristiantaksdal/repos/power-system-data/Øving_5/ProductionConsumption-2026.csv',
    parse_dates=['Time(Local)']
)

#Ordner opp i tidssoner og setter tidssone til lokal Norge-tid
df.columns = df.columns.str.strip()
df['Time(Local)'] = pd.to_datetime(
    df['Time(Local)'],
    format="%d.%m.%Y %H:%M:%S %z",
    dayfirst=True,
    utc=True  
)
df = df.set_index('Time(Local)')
df = df.tz_convert("Europe/Oslo")


dogn_profil = df.loc["2026-03-03"]

t = np.linspace(0, 23, 24)

#Setter base load til å være på starten av dagen
base_load = 17000

morning_peak = 2100 * np.exp(-0.5*((t-8)/2)**2)
evening_peak = 1800 * np.exp(-0.5*((t-19)/4.5)**2)
night_decline =  -800 * np.exp(-0.5*((t-4)/2)**2)

model_load = (
    base_load
    + night_decline
    + morning_peak
    + evening_peak
)

x = range(len(dogn_profil.index))

#Figur for et døgn, observert og modell
plt.figure(figsize=(10,5))

plt.plot(x,
    dogn_profil["Consumption"],
    label="Consumption",
    marker='o'
)

plt.plot(x,
    model_load,
    label="Modell",
    marker = "o"
)

plt.title("Forbruk, observert og modell")
plt.xlabel("Timer")
plt.xticks(x)
plt.ylabel("Effekt [MW]")
plt.grid(True)
plt.legend()
plt.savefig("/Users/olekristiantaksdal/repos/power-system-data/Øving_5/obs_og_mod")
plt.show()

#Figur for et døgn, observert
plt.figure(figsize=(10,5))

plt.plot(x,
    dogn_profil["Consumption"],
    label="Consumption",
    marker='o'
)

plt.title("Forbruk observert")
plt.xlabel("Timer")
plt.xticks(x)
plt.ylabel("Effekt [MW]")
plt.grid(True)
plt.legend()
plt.savefig("/Users/olekristiantaksdal/repos/power-system-data/Øving_5/forbruk_observert")
plt.show()

plt.figure(figsize=(10,5))

plt.plot(x,
    model_load,
    label="Modell",
    marker = "o",
    color= "orange",
)

plt.plot(x,
    night_decline + base_load,
    label = "Night decline",
    linestyle = ":"
)

plt.plot(x,
    morning_peak + base_load,
    label = "Morning peak",
    linestyle = ":"
)

plt.plot(x,
    evening_peak + base_load,
    label = "Evening peak",
    linestyle = ":"
)

plt.title("Forbruk, modell")
plt.xlabel("Timer")
plt.xticks(x)
plt.ylabel("Effekt [MW]")
plt.grid(True)
plt.legend()
plt.savefig("/Users/olekristiantaksdal/repos/power-system-data/Øving_5/modell")
plt.show()

plt.figure(figsize=(10,5))

plt.plot(x,
    dogn_profil["Consumption"],
    label="Consumption",
    marker='o'
)

plt.plot(x,
    model_load,
    label="Modell",
    marker = "o",
    color= "orange",
)

plt.plot(x,
    night_decline + base_load,
    label = "Night decline",
    linestyle = ":"
)

plt.plot(x,
    morning_peak + base_load,
    label = "Morning peak",
    linestyle = ":"
)

plt.plot(x,
    evening_peak + base_load,
    label = "Evening peak",
    linestyle = ":"
)

plt.title("Forbruk, modell")
plt.xlabel("Timer")
plt.xticks(x)
plt.ylabel("Effekt [MW]")
plt.grid(True)
plt.legend()
plt.savefig("/Users/olekristiantaksdal/repos/power-system-data/Øving_5/obs_med_full_modell")
plt.show()