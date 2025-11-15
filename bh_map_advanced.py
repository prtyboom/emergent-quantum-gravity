import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster  # For clustering

# Sample real BH data (RA in deg, Dec in deg; expand with CSV)
bh_data = [
    {'name': 'GW150914', 'ra': 162.25, 'dec': -23.38},  # Real coords
    {'name': 'M87*', 'ra': 187.71, 'dec': 12.39},
    {'name': 'Sgr A*', 'ra': 266.42, 'dec': -29.01},
    {'name': '3C 273', 'ra': 187.28, 'dec': 2.05},
    {'name': 'GW190521', 'ra': 202.5, 'dec': 33.0},
    # Add ~10 more for demo (real quasars/GW)
    {'name': 'Quasar1', 'ra': 180.0, 'dec': 10.0},
    {'name': 'GW170817', 'ra': 197.45, 'dec': -23.38},
    {'name': 'Quasar2', 'ra': 190.0, 'dec': 15.0},
    {'name': 'GW200129', 'ra': 185.0, 'dec': 5.0},
    {'name': 'Quasar3', 'ra': 200.0, 'dec': -20.0},
    # ... Add from CSV for full analysis
]

# Convert to SkyCoord
coords = SkyCoord(ra=[d['ra'] for d in bh_data] * u.deg, dec=[d['dec'] for d in bh_data] * u.deg, frame='icrs')

# Mollweide projection
ra_rad = coords.ra.wrap_at(180 * u.deg).radian
dec_rad = coords.dec.radian

# Clustering (hierarchical)
positions = np.column_stack((ra_rad, dec_rad))
Z = linkage(positions, method='ward')
clusters = fcluster(Z, t=1.0, criterion='distance')  # t=1.0 for ~10° clusters

# Plot
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='mollweide')
scatter = ax.scatter(ra_rad, dec_rad, c=clusters, cmap='viridis', s=50, label='Black Holes')

# Annotations
ax.annotate('Пример Дуги', xy=(np.deg2rad(150-180), np.deg2rad(-20)), xytext=(np.deg2rad(120-180), np.deg2rad(-30)),
            arrowprops=dict(facecolor='red', shrink=0.05), color='red')
ax.annotate('Кластер', xy=(np.deg2rad(180-180), np.deg2rad(10)), xytext=(np.deg2rad(150-180), np.deg2rad(20)),
            arrowprops=dict(facecolor='green', shrink=0.05), color='green')
ax.annotate('Пустота', xy=(np.deg2rad(0), np.deg2rad(0)), xytext=(np.deg2rad(-30), np.deg2rad(10)),
            arrowprops=dict(facecolor='orange', shrink=0.05), color='orange')

ax.set_title('Карта Расположения Чёрных Дыр на "Пленке" (Мембране)')
ax.set_xlabel('Прямое Восхождение (RA, в радианах от -π до π)')
ax.set_ylabel('Склонение (Dec)')
ax.grid(True)
plt.colorbar(scatter, label='Кластер ID')
plt.legend()
plt.savefig('bh_membrane_map.png')
plt.show()

# Simple stats output to TXT
with open('bh_analysis.txt', 'w') as f:
    f.write(f'Всего ЧД: {len(bh_data)}\n')
    f.write(f'Число кластеров: {len(np.unique(clusters))}\n')
    f.write('Паттерны: Ищите дуги в RA 150-200, voids в RA 0-50.\n')