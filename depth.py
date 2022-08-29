#!/usr/bin/python3

import time
import sys
import csv # needed to create csv file
import signal
sys.path.append("/usr/bin") # needed to locate ms5837 file (actually probably don't need this anymore)
import ms5837 #sensor library provided by blue robotics
import prctl

sensor = ms5837.MS5837_30BA(0) # Specify I2C bus 0

# We must initialize the sensor before reading it
if not sensor.init():
    print("Sensor could not be initialized")
    exit(1)

with open('/mnt/data/depth.csv', 'a') as f:
    allow_run = True
    def sigterm_handler(signal, frame):
        global allow_run # Bad pattern.  TODO: fix
        allow_run = False

    prctl.set_pdeathsig(signal.SIGTERM)
    signal.signal(signal.SIGTERM, sigterm_handler)

    writer = csv.writer(f)

    # write the header
    header = ['pressure (atm)', 'temperature (F)', 'depth (m)']
    writer.writerow(header)

    while allow_run:
        # We have to read values from sensor to update pressure and temperature
        if not sensor.read():
            print("Sensor read failed!")
            exit(1)

        # print("Pressure: %.2f atm") % (
        # sensor.pressure(ms5837.UNITS_atm)) #f strings

        # print("Temperature: %.2f C  %.2f F") % (
        # sensor.temperature(ms5837.UNITS_Centigrade),
        # sensor.temperature(ms5837.UNITS_Farenheit))

        freshwaterDepth = sensor.depth() # default is freshwater
        sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
        saltwaterDepth = sensor.depth() # No nead to read() again
        sensor.setFluidDensity(1000) # kg/m^3
        # print("Depth:  %.3f m (saltwater)") % (saltwaterDepth)

        # fluidDensity doesn't matter for altitude() (always MSL air density)
        # print("MSL Relative Altitude: %.2f m") % sensor.altitude() # relative to Mean Sea Level pressure in air

        sensorPressure = sensor.pressure(ms5837.UNITS_atm)
        sensorTemperature = sensor.temperature(ms5837.UNITS_Farenheit)

        #csv creation
        data = [sensorPressure, sensorTemperature, saltwaterDepth]

        # write the data
        writer.writerow(data)
    f.flush()
    #csv creation done
