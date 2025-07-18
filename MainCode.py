from tkinter import *
import lightkurve as lk
import numpy as np
import threading
import matplotlib.pyplot as plt
from exoplanetml import predict_exoplanet_status
import pandas as pd
def upload_page():
    global address, result_label
    upload_root = Tk()
    upload_root.title('Upload')
    address = StringVar()
    result_label = Label(upload_root, text="", font=("verdana", 15))
    
    label1 = Label(upload_root, text="Upload Light Intensity Data", width=100, font=("freestyle script", 50))
    label1.pack()
    Label(upload_root, text="").pack()
    Label(upload_root, text="").pack()
    Label(upload_root, text="").pack()
    Label(upload_root, text="").pack()
    
    entry1 = Entry(upload_root, textvariable=address, width=40, font=("verdana", 15))
    entry1.pack()
    
    Label(upload_root, text="").pack()
    Label(upload_root, text="").pack()
    Label(upload_root, text="").pack()
    
    Button(upload_root, text="Submit", width=20, cursor='hand2', height=2, command=launch_compute).pack()
    
    result_label.pack()
    
    upload_root.mainloop()

def launch_compute():
    # Start the compute function in a separate thread
    compute_thread = threading.Thread(target=compute)
    compute_thread.start()

def test(s):
    result_label.config(text=f"Planet Period: {planet_x_period}\nTransit Time: {planet_x_t0}\nTransit Duration: {planet_x_dur}\nExoplanet Radius: {np.sqrt((planet_x_dur * planet_x_period) / np.pi)}\nIt "+s+" a exoplanet")
    

def compute():
    # Provide the correct path to the FITS file
    pixel_file_path = address.get()
    
    try:
        pixelFile = lk.open(pixel_file_path)
    except FileNotFoundError:
        result_label.config(text="File not found.")
        return

    

    lc = pixelFile.to_lightcurve(aperture_mask=pixelFile.pipeline_mask)

    flat_lc = lc.flatten()
    time_values = flat_lc.time.value
    flux_values = flat_lc.flux.value
    plt.plot(time_values, flux_values, 'b.-', markersize=2)
    plt.xlabel('Time')
    plt.ylabel('Flux')
    plt.title('Flattened Light Curve')
    plt.show()
    folded_lc = flat_lc.fold(period=3.5225)

    period = np.linspace(1, 5, 10000)
    bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500)
    global planet_x_period
    global planet_x_t0
    global planet_x_dur
    global exoplanetradius
    planet_x_period = bls.period_at_max_power.value
    planet_x_t0 = bls.transit_time_at_max_power.value
    planet_x_dur = bls.duration_at_max_power.value
    exoplanetradius = np.sqrt((planet_x_dur * planet_x_period) / np.pi)
    ax = lc.fold(period=planet_x_period, epoch_time=planet_x_t0).scatter()
    ax.set_xlim(-2, 2)

    
    features = pd.DataFrame({'Orbital period': [planet_x_period],
                         'transit duration': [planet_x_dur],
                         'radii(planet)': [exoplanetradius]})

    exo_status = predict_exoplanet_status(features)

    if exo_status == "CONFIRMED" or exo_status == "CANDIDATE":
        test("is")
    else:
        test("is not")


upload_page() 
