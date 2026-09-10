import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone
import time

df = pd.read_csv('/Users/olekristiantaksdal/repos/power-system-data/Øving_4/load_data.csv',
    decimal=",",
    parse_dates=['Time(Local)']
)

df.columns = df.columns.str.strip()
df['Time(Local)'] = pd.to_datetime(
    df['Time(Local)'],
    format="%d.%m.%Y %H:%M:%S %z",
    dayfirst=True,
    utc=True  
)
df = df.set_index('Time(Local)')

#df = df.sort_index()

df = df.tz_convert("Europe/Oslo")

df["Netto"] = (df["Production"] - df["Consumption"])
tot_prod = df["Production"].sum()
tot_prod = tot_prod*10**(-3)

print("De første fem linjene:")
print(df.head())

print("Indeks 0:")
print(df.index[0])

print("Info for kl 03:00:")
print(df.loc["2026-03-03 03:00"])

#dogn_profil = df.loc["2026-01-01 00:00":"2026-01-01 23:59"]
dogn_profil = df.loc["2026-03-03"]

max_prod = max(dogn_profil["Production"])
min_prod = min(dogn_profil["Production"])

max_netto = round(max(dogn_profil["Netto"]), 2)
min_netto = round(min(dogn_profil["Netto"]), 2)

tid_max = dogn_profil["Netto"].idxmax()
tid_min = dogn_profil["Netto"].idxmin()
print(tid_max)
print(tid_min)
print("Max prod =", max_prod, "MW og min prod =", min_prod, "MW")
print("Max netto =", max_netto, "MW, som skjer klokken", tid_max,
    " og min netto =", min_netto, "MW, som skjer klokken", tid_min
)
print("Total produksjon i løpet av et døgn er", tot_prod, "GW")

x = range(len(dogn_profil.index))
x2 = range(len(df.index))

#Figur for et døgn
plt.figure(figsize=(10,5))

plt.plot(x,
    dogn_profil["Consumption"],
    label="Consumption",
    marker='o'
)

plt.plot(x, 
    dogn_profil["Production"], 
    label="Production", 
    marker = "o"
)

plt.plot(x, 
    dogn_profil["Netto"],
    label = "Netto",
    marker = "o"
)

# df.plot(dogn_profil)
plt.title("Produksjon og forbruk")
plt.xlabel("Timer")
plt.xticks(x)
plt.ylabel("Effekt [MW]")
plt.grid(True)
plt.legend()
plt.show()

#Figur med produksjon og forbruk
plt.figure(figsize=(10,5))

plt.plot(df.index,
    df["Production"],
    label= "Production"
)

plt.plot(df.index,
    df["Consumption"],
    label="Consumption"
)

# df.plot(
#     y=["Production", "Consumption"],
#     figsize = (10, 5)
# )

plt.title("Produksjon og forbruk for hele året")
plt.xlabel("Tid")

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.ylabel("Effekt [MW]")
plt.grid(True)
plt.legend()
plt.show()

#Plotting av produksjon, forbruk og netto   
plt.figure(figsize=(10,5))

plt.plot(df.index,
    df["Production"],
    label= "Production"
)

plt.plot(df.index,
    df["Consumption"],
    label="Consumption"
)

plt.plot(df.index,
    df["Netto"],
    label = "Netto"
)

# df.plot(
#     y=["Production", "Consumption"],
#     figsize = (10, 5)
# )

plt.title("Produksjon, forbruk og netto for hele året")
plt.xlabel("Tid")

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

plt.ylabel("Effekt [MW]")
plt.grid(True)
plt.legend()
plt.show()