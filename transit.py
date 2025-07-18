from lightkurve import search_targetpixelfile
from lightkurve import TessTargetPixelFile
import lightkurve as lc
import numpy as np

pixelFile = search_targetpixelfile('KIC 6922244', author="Kepler", cadence="long", quarter=4).download()
pixelFile.plot(frame=42)

lc = pixelFile.to_lightcurve(aperture_mask=pixelFile.pipeline_mask)
lc.plot()

flat_lc = lc.flatten()
flat_lc.plot()

folded_lc = flat_lc.fold(period=3.5225)
folded_lc.plot()

period = np.linspace(1, 5, 10000)
bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500)
bls.plot()

planet_x_period = bls.period_at_max_power

planet_x_t0 = bls.transit_time_at_max_power
planet_x_dur = bls.duration_at_max_power

ax = lc.fold(period=planet_x_period, epoch_time=planet_x_t0).scatter()
ax.set_xlim(-2,2)

print(planet_x_period)
print(planet_x_t0)
print(planet_x_dur)

exoplanet_radius = np.sqrt((planet_x_dur *planet_x_period ) /np.pi )

