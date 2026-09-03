import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import time

#Leser csv filen
df = pd.read_csv('/Users/olekristiantaksdal/repos/power-system-data/load/forbruk_2025.csv', parse_dates=['Time'])

#Gjør date-time objektene om til rett format
df.columns = df.columns.str.strip()

df['Time'] = pd.to_datetime(
    df["Time"],
    dayfirst=True,
    utc=True  
)

df = df.set_index("Time")
df = df.sort_index()

df = df.tz_convert("Europe/Oslo")

#Deler opp for hver måned og finner gjennomsnitt
monthly = df['Actual Load'].resample("1M").mean()
alle_verdier = df['Actual Load']

#For å få hver måned på x-aksen og ikke noen tilfeldige datoer
month_labels = monthly.index.strftime('%b')
x = range(len(monthly.index))

#Plotting av figur
plt.figure(figsize=(10,4))
plt.plot(x, monthly.values, marker='o')
plt.title("Forbruk")
plt.xlabel("Måneder")
plt.xticks(x, month_labels)
plt.ylabel("Effekt [MW]")
plt.grid(True)
plt.legend()

#Lager filer
plt.savefig('/Users/olekristiantaksdal/repos/power-system-data/Results/figur.png')

plt.show()

monthly.to_csv('/Users/olekristiantaksdal/repos/power-system-data/Results/resultater.csv')

#Finner max og min
#hoyest_last = max(alle_verdier)
#lavest_last = min(alle_verdier)

#Finner standardavvik og max og min
std = df['Actual Load'].resample('1M').std()
hoyest_last = df['Actual Load'].resample('1M').max()
lavest_last = df['Actual Load'].resample('1M').min()

info = pd.DataFrame({"Høyest last":hoyest_last, "Lavest last":lavest_last, "Standardavvik":std})
info.to_csv('/Users/olekristiantaksdal/repos/power-system-data/Results/statistikk.csv')
#print('Max-verdi:', hoyest_last)
#print('Min-verdi:', lavest_last)
#print('Standardavvik for hver måned:')
#print(std)