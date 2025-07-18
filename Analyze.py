from tkinter import *
from lightkurve import search_targetpixelfile
from lightkurve import TessTargetPixelFile
import lightkurve as lc
import numpy as np


def upload_page():
    global address
    upload_root=Tk()
    upload_root.title('Upload')
    address=StringVar()
    label1 =Label(upload_root, text="Upload Light Intensity Data",width=100, font=("freestyle script", 50)).pack()
    Label(upload_root, text="",).pack()
    Label(upload_root, text="",).pack()
    Label(upload_root, text="",).pack()
    Label(upload_root, text="",).pack()
    entry1=Entry(upload_root,textvariable=address,width=40,font=("verdana",15)).pack()
    Label(upload_root, text="",).pack()
    Label(upload_root, text="",).pack()
    Label(upload_root, text="",).pack()
    Button(upload_root, text="submit", width=20,cursor='hand2', height=2,command=compute).pack()
    upload_root.mainloop()

def compute():

    pixelFile = input(address)
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


upload_page()

