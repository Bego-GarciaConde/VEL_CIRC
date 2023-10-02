import pandas as pd
import numpy as np

        ##################################################
        #                     Settings                   #
        ##################################################



limit = 50 #limit for acceleration mesh
G= 1.3273e11
kpc_to_km= 3.086e16
seconds_to_Myr = 3.15576e+16
softening = 0


snapshots_analysis = [620]



# ---------------------------------------------------------------------------
#path_satellite_models = "/media/temp1/bego/snapshots/modelos_satelites/"
path_csv = "/home/bego/GARROTXA/snapshots/"
path_datos = "/home/bego/GARROTXA/datos_GARROTXA_resim/"
#path_crossmatch = "/mnt/usb-TOSHIBA_EXTERNAL_USB_20220124010088F-0:0-part2/satelites_crossmatch/"
#path_figures_acceleration = "/home/bego/GARROTXA/aceleration_figures/"
#path_figures = "/home/bego/GARROTXA/acceleration_figures/"
#path_acceleration = "/home/bego/GARROTXA/acceleration/"
#path_disk = "/home/bego/GARROTXA/disco/"
#path_results = "/home/bego/GARROTXA/GalaDyn/results/"
#path_figures_bending = "/home/bego/GARROTXA/BendingBreathing/"

#----------------------------------------------------------------------------
satelites = ["arania", "grillo", "mosquito", "all"]


datos_edades = pd.read_csv(path_datos + "edades.csv", sep = ",",index_col = 0)
lookback = [datos_edades.loc[datos_edades['Snapshot'] == name, 'Lookback'].iloc[0] for name in snapshots_analysis]