import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone
import time

df = pd.read_csv("/Users/olekristiantaksdal/repos/power-system-data/Øving_6/faktisk_skikkelig_soldata_på_hyttå_for_real_this_time.csv",
    skiprows=8,
    skipfooter=10,
    dayfirst=True,
    parse_dates=["time"])

#Ordner opp i tidssoner og setter tidssone til lokal Norge-tid
df["time"] = (pd.to_datetime(df["time"], 
    format="%Y%m%d:%H%M").dt.round("h")
)

df["time"] = pd.to_datetime(df["time"],
    utc=True
)

df = df.set_index('time')
df = df.tz_convert("Europe/Oslo")

df2 = pd.read_csv("/Users/olekristiantaksdal/repos/power-system-data/Øving_6/faktisk_skikkelig_soldata_på_hyttå_for_real_for_real_this_time_med_optimized_greier.csv",
    skiprows=8,
    skipfooter=10,
    dayfirst=True,
    parse_dates=["time"]
)

#Ordner opp i tidssoner og setter tidssone til lokal Norge-tid
df2["time"] = (pd.to_datetime(df2["time"], 
    format="%Y%m%d:%H%M").dt.round("h")
)

df2["time"] = pd.to_datetime(df2["time"],
    utc=True
)

df2 = df2.set_index('time')
df2 = df2.tz_convert("Europe/Oslo")

print(df.head())

#max_innstråling = max(innstråling)
tid_max = df["G(i)"].idxmax()
#date_max = tid_max.strftime('%Y-%m-%d')
print("max innstråling skjer", tid_max)
dag = df.loc['2022-06-05']
dag2 = df2.loc['2022-06-05']
month = df2.loc['2022-06']

t = np.linspace(0, 23, 500)
t2 = np.linspace(0, 23, 24)

A = 800
mu = 13
sigma = 3
sigma_okt = 4

A3 = 1100
mu3 = 14
sigma_3 = 3

G = A * np.exp(-(t - mu)**2 / (2 * sigma**2))
G2 = A *np.exp(-(t-mu)**2 / (2 * sigma_okt**2))
G3 = A3 *np.exp(-(t-mu3)**2 / (2 * sigma_3**2))

x = range(len(dag.index))
x2 = range(len(dag2.index))
x3 = range(len(month.index))

# Plotting av utregnet modell
plt.plot(t, G, label="Kurve 1")
plt.plot(t, G2, label="Kurve 2")
plt.xlabel("Tid [timer]")
plt.ylabel("Innstråling [W/m²]")
plt.xticks(x)
plt.legend()
plt.grid()
plt.savefig("/Users/olekristiantaksdal/repos/power-system-data/Øving_6/fig_modell")
plt.show()

# Plotting av hele året
df2.plot(
    y = ["G(i)"],
    figsize = (10, 5)
)
plt.xlabel("Tid [timer]")
plt.ylabel("Innstråling [W/m²]")
plt.legend()
plt.grid()
plt.savefig("/Users/olekristiantaksdal/repos/power-system-data/Øving_6/fig_år")
plt.show()

# Plotting av juni måned
month.plot(
    y = ["G(i)"],
    figsize=(10,5)
)
plt.xlabel("Tid [timer]")
plt.ylabel("Innstråling [W/m²]")
plt.legend()
plt.grid()
plt.savefig("/Users/olekristiantaksdal/repos/power-system-data/Øving_6/fig_juni")
plt.show()

# Plotting av dag med optimized slope og azimiuth
plt.plot(x2,
    dag2["G(i)"],
    label = "innstråling, optimized",
    marker = "o",
)
plt.plot(x,
    dag["G(i)"],
    label = "innstråling, egendefinert",
    marker = "o",
)
plt.xlabel("Tid [timer]")
plt.ylabel("Innstråling [W/m²]")
plt.xticks(x)
plt.legend()
plt.grid()
plt.savefig("/Users/olekristiantaksdal/repos/power-system-data/Øving_6/fig_sammenligning")
plt.show()

# Plotting av Gauss og data i samme fig
plt.plot(x2,
    dag2["G(i)"],
    label = "innstråling",
    marker = "o",
)
plt.plot(t,
    G3,
    label = "Gauss-modell"
)
plt.xlabel("Tid [timer]")
plt.ylabel("Innstråling [W/m²]")
plt.xticks(x)
plt.legend()
plt.grid()
plt.savefig("/Users/olekristiantaksdal/repos/power-system-data/Øving_6/fig_gauss_og_data")
plt.show()