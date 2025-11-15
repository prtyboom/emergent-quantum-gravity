import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.stats import poisson
try:
    from gwosc import datasets
except ImportError:
    datasets = None
import pandas as pd
import plotly.graph_objects as go

# Загрузка событий
bh_data = []
if datasets:
    try:
        events = datasets.find_datasets(type='event')
        filtered_events = [event for event in events if 'GW' in event and ('3' in event or '2' in event)]
        print(f'Загружено {len(filtered_events)} событий из GWOSC.')
        for event in filtered_events:
            ra = np.random.uniform(0, 360)  # Случайно для demo; замените на реальные
            dec = np.random.uniform(-90, 90)
            bh_data.append({'name': event, 'ra': ra, 'dec': dec})  # 'name' added explicitly
    except Exception as e:
        print(f'Ошибка GWOSC: {e} - Используем sample data.')

# Fallback, если данных нет
if not bh_data:
    print('Данных нет - используем sample.')
    bh_data = [
        {'name': 'GW150914', 'ra': 162.25, 'dec': -23.38},
        {'name': 'M87*', 'ra': 187.71, 'dec': 12.39},
        {'name': 'Sgr A*', 'ra': 266.42, 'dec': -29.01},
        {'name': '3C 273', 'ra': 187.28, 'dec': 2.05},
        {'name': 'GW190521', 'ra': 202.5, 'dec': 33.0},
        {'name': 'Quasar1', 'ra': 180.0, 'dec': 10.0},
        {'name': 'GW170817', 'ra': 197.45, 'dec': -23.38},
        {'name': 'Quasar2', 'ra': 190.0, 'dec': 15.0},
        {'name': 'GW200129', 'ra': 185.0, 'dec': 5.0},
        {'name': 'Quasar3', 'ra': 200.0, 'dec': -20.0},
    ]

# Очистка invalid dec
bh_data = [d for d in bh_data if abs(d['dec']) <= 90]
n_points = len(bh_data)

# Конвертация в координаты
coords = SkyCoord(ra=[d['ra'] for d in bh_data] * u.deg, dec=[d['dec'] for d in bh_data] * u.deg, frame='icrs')

# Проекция
ra_rad = coords.ra.wrap_at(180 * u.deg).radian
dec_rad = coords.dec.radian

# Малый jitter
ra_rad += np.random.normal(0, 0.01, n_points)
dec_rad += np.random.normal(0, 0.01, n_points)
dec_rad = np.clip(dec_rad, -np.pi/2, np.pi/2)

# Кластеризация
positions = np.column_stack((ra_rad, dec_rad))
db = DBSCAN(eps=0.3, min_samples=3).fit(positions)
clusters = db.labels_
unique_clusters = np.unique(clusters[clusters >= 0])

# Monte-Carlo p-value
n_sim = 100
max_densities = []
for _ in range(n_sim):
    sim_ra = np.random.uniform(-np.pi, np.pi, n_points)
    sim_dec = np.arcsin(np.random.uniform(-1, 1, n_points))
    sim_pos = np.column_stack((sim_ra, sim_dec))
    sim_db = DBSCAN(eps=0.3, min_samples=3).fit(sim_pos)
    sim_clusters = sim_db.labels_
    sim_unique = np.unique(sim_clusters[sim_clusters >= 0])
    sim_density = max([np.sum(sim_clusters == c) for c in sim_unique]) if len(sim_unique) > 0 else 0
    max_densities.append(sim_density)
observed_density = max([np.sum(clusters == c) for c in unique_clusters]) if len(unique_clusters) > 0 else 0
p_value = np.sum(np.array(max_densities) >= observed_density) / n_sim
print(f'Monte-Carlo p-value: {p_value}')

# 2D Plot
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='mollweide')
scatter = ax.scatter(ra_rad, dec_rad, c=clusters, cmap='viridis', s=30, label='Black Holes')
ax.set_title('v3 Карта с Кластеризацией и P-value')
ax.grid(True)
plt.colorbar(scatter, label='Cluster ID')
plt.savefig('bh_map_v3.png')
plt.show()

# 3D Interactive Plot with Visible Sphere
# Данные для точек
df = pd.DataFrame({'ra': [d['ra'] for d in bh_data], 'dec': [d['dec'] for d in bh_data], 'cluster': clusters, 'name': [d.get('name', 'Unknown') for d in bh_data]})  # Safe 'name'

# Конвертация в Cartesian
theta = np.deg2rad(df['dec'] + 90)
phi = np.deg2rad(df['ra'])
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

# Фигура
fig3d = go.Figure()

# Точки
fig3d.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=5, color=df['cluster'], colorscale='viridis', colorbar_title='Cluster ID'), text=df['name'], name='Black Holes'))

# Прозрачная сфера
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
sx = np.outer(np.cos(u), np.sin(v))
sy = np.outer(np.sin(u), np.sin(v))
sz = np.outer(np.ones(np.size(u)), np.cos(v))
fig3d.add_trace(go.Surface(x=sx, y=sy, z=sz, opacity=0.2, colorscale='blues', showscale=False, name='Мембрана Сфера'))

fig3d.update_layout(title='3D Интерактивная Карта ЧД на Сфере Мембраны', scene=dict(aspectmode='cube'))
fig3d.show()
print('3D с сферой открыто!')

# Отчёт
with open('bh_analysis_v3.txt', 'w') as f:
    f.write(f'Всего точек: {n_points}\n')
    f.write(f'Число кластеров: {len(unique_clusters)}\n')
    f.write(f'P-value (неслучайность): {p_value}\n')
    f.write('Если p < 0.05, распределение неслучайно!\n')