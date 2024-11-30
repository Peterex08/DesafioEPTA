import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg

#Código mei fei, ver se dá pra melhorar depois
#all rights reserved to manga

logo_epta = mpimg.imread('../media/EPTA - Azul.png') 

gps_data = pd.ExcelFile('dados telemetria foguete real.xlsx')

gps_cleaned = gps_data.parse('GPS Data')

gps_cleaned.columns = ["Longitude", "Latitude", "Altitude (m)", 
                       "Counter", "East (ft)", "North (ft)", "Altitude (ft)","Altitude (ft)",
                       "Time (s)", "Offset Time (s)", "Vertical Velocity (fps)", 
                       "Vertical Velocity (mph)", "Distance Traveled", 
                       "Ground Velocity (mph)", "Acceleration (g)"]

gps_cleaned = gps_cleaned[["Longitude", "Latitude", "Altitude (m)", "Time (s)"]]

gps_cleaned = gps_cleaned.apply(pd.to_numeric, errors="coerce")
gps_cleaned = gps_cleaned.dropna()

longitude = gps_cleaned['Longitude'].values
latitude = gps_cleaned['Latitude'].values
altitude = gps_cleaned['Altitude (m)'].values
time = gps_cleaned['Time (s)'].values

ab_paradiff = np.argmin(np.diff(altitude) / np.diff(time))
ab_parapogeu = np.argmax(altitude)

fig = plt.figure(figsize=(15, 10))
ax3d = fig.add_subplot(221, projection='3d')
ax_lat = fig.add_subplot(222)
ax_lon = fig.add_subplot(223)
ax_alt = fig.add_subplot(224)

ax3d.set_xlim([min(longitude), max(longitude)])
ax3d.set_ylim([min(latitude), max(latitude)])
ax3d.set_zlim([min(altitude), max(altitude)])

ax_lat.imshow(logo_epta, extent=[min(time), max(time), min(latitude), max(latitude)], aspect='auto', alpha=0.5)
ax_lat.set_xlim([min(time), max(time)])
ax_lat.set_ylim([min(latitude), max(latitude)])

ax_lon.imshow(logo_epta, extent=[min(time), max(time), min(longitude), max(longitude)], aspect='auto', alpha=0.5)
ax_lon.set_xlim([min(time), max(time)])
ax_lon.set_ylim([min(longitude), max(longitude)])

ax_alt.imshow(logo_epta, extent=[min(time), max(time), min(altitude), max(altitude)], aspect='auto', alpha=0.5)
ax_alt.set_xlim([min(time), max(time)])
ax_alt.set_ylim([min(altitude), max(altitude)])


ax3d.set_xlabel('Longitude')
ax3d.set_ylabel('Latitude')
ax3d.set_zlabel('Altitude (m)')
ax3d.set_title('Trajetória 3D')

ax_lat.set_xlabel('Tempo (s)')
ax_lat.set_ylabel('Latitude')
ax_lat.set_title('Latitude vs Tempo')

ax_lon.set_xlabel('Tempo (s)')
ax_lon.set_ylabel('Longitude')
ax_lon.set_title('Longitude vs Tempo')

ax_alt.set_xlabel('Tempo (s)')
ax_alt.set_ylabel('Altitude (m)')
ax_alt.set_title('Altitude vs Tempo')


def novo_frame(frame):
    
    ax3d.cla()
    ax_lat.cla()
    ax_lon.cla()
    ax_alt.cla()
    
    ax3d.set_xlim([min(longitude), max(longitude)])
    ax3d.set_ylim([min(latitude), max(latitude)])
    ax3d.set_zlim([min(altitude), max(altitude)])
    ax3d.set_xlabel('Longitude')
    ax3d.set_ylabel('Latitude')
    ax3d.set_zlabel('Altitude (m)')
    ax3d.set_title('Trajetória 3D')

    ax_lat.imshow(logo_epta, extent=[min(time), max(time), min(latitude), max(latitude)], aspect='auto', alpha=0.5)
    ax_lat.set_xlim([min(time), max(time)])
    ax_lat.set_ylim([min(latitude), max(latitude)])
    ax_lat.set_xlabel('Tempo (s)')
    ax_lat.set_ylabel('Latitude')
    ax_lat.set_title('Latitude vs Tempo')
    
    ax_lon.imshow(logo_epta, extent=[min(time), max(time), min(longitude), max(longitude)], aspect='auto', alpha=0.5)
    ax_lon.set_xlim([min(time), max(time)])
    ax_lon.set_ylim([min(longitude), max(longitude)])
    ax_lon.set_xlabel('Tempo (s)')
    ax_lon.set_ylabel('Longitude')
    ax_lon.set_title('Longitude vs Tempo')
    
    ax_alt.imshow(logo_epta, extent=[min(time), max(time), min(altitude), max(altitude)], aspect='auto', alpha=0.5)
    ax_alt.set_xlim([min(time), max(time)])
    ax_alt.set_ylim([min(altitude), max(altitude)])
    ax_alt.set_xlabel('Tempo (s)')
    ax_alt.set_ylabel('Altitude (m)')
    ax_alt.set_title('Altitude vs Tempo')
    
    ax3d.plot(longitude[:frame], latitude[:frame], altitude[:frame], color='b', marker='o')
    if frame > ab_parapogeu:
        ax3d.scatter(longitude[ab_parapogeu], latitude[ab_parapogeu], altitude[ab_parapogeu],
                     color='g', s=50, label="Abertura Paraquedas (Apogeu)")
        ax3d.legend()
        ax3d.scatter(longitude[ab_paradiff], latitude[ab_paradiff], altitude[ab_paradiff],
                     color='r', s=50, label="Abertura Paraquedas (Diff)")
        ax3d.legend()
    
    ax_lat.plot(time[:frame], latitude[:frame], color='b')
    if frame > ab_paradiff:
        ax_lat.scatter(time[ab_parapogeu], latitude[ab_parapogeu], color='g', s=50)
        ax_lat.scatter(time[ab_paradiff], latitude[ab_paradiff], color='r', s=50)
    
    ax_lon.plot(time[:frame], longitude[:frame], color='b')
    if frame > ab_paradiff:
        ax_lon.scatter(time[ab_parapogeu], longitude[ab_parapogeu], color='g', s=50)
        ax_lon.scatter(time[ab_paradiff], longitude[ab_paradiff], color='r', s=50)
 
    ax_alt.plot(time[:frame], altitude[:frame], color='b')
    if frame > ab_paradiff:
        ax_alt.scatter(time[ab_parapogeu], altitude[ab_parapogeu], color='g', s=50)
        ax_alt.scatter(time[ab_paradiff], altitude[ab_paradiff], color='r', s=50)
    
    return ax3d, ax_lat, ax_lon, ax_alt

ani = FuncAnimation(fig, novo_frame, frames=len(time), interval=100, blit=False)

plt.tight_layout()
plt.show()

#trembão é coisa boa