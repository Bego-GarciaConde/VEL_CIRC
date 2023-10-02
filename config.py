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

PATH_CSV = "/home/bego/GARROTXA/snapshots/"
PATH_DATOS = "/home/bego/GARROTXA/datos_GARROTXA_resim/"
PATH_DISK = "/home/bego/GARROTXA/disco/"


#----------------------------------------------------------------------------
satelites = ["arania", "grillo", "mosquito", "all"]


datos_edades = pd.read_csv(PATH_DATOS + "edades.csv", sep =",", index_col = 0)
lookback = [datos_edades.loc[datos_edades['Snapshot'] == name, 'Lookback'].iloc[0] for name in snapshots_analysis]