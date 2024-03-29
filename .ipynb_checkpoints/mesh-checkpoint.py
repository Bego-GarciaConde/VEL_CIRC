
import numpy as np
import pandas as pd
import gc
from multiprocessing import Pool
from config import *
import matplotlib.pyplot as plt
from itertools import repeat
from functools import partial
import concurrent.futures
import multiprocessing
import sys
import uuid
from scipy import stats
import sys
sys.path.append('../')

from progress_bar import progressbar

from snapshot import Snapshot

def force_in_mesh_gen (coord, x_0, y_0, z_0, mass_0):
    #a = GM/(r²)     <----
    i,j,k = coord[0], coord[1], coord[2]
   # r_sph = np.sqrt(i**2 +j**2 + k**2)
    r_sph = 30
    ind = np.where(np.sqrt(x_0**2+y_0**2 + z_0**2)<r_sph)
    X_resta = (x_0[ind] - i)
    Y_resta = (y_0[ind] - j)
    Z_resta = (z_0[ind] - k)
    
    dist_sat_part = np.sqrt(X_resta**2 + Y_resta**2 + Z_resta**2)


    ax = (mass_0[ind]*X_resta/np.power(dist_sat_part,3)).astype(np.float64)
    ay = (mass_0[ind]*Y_resta/np.power(dist_sat_part,3)).astype(np.float64)

    return [G*np.sum(ax)/(kpc_to_km**2), G*np.sum(ay)/(kpc_to_km**2)]

def extract_coord_mass (data):
    x = np.array(data["X"], dtype = np.float32)
    y = np.array(data["Y"], dtype = np.float32)
    z = np.array(data["Z"], dtype = np.float32)

    mass = np.array(data["Mass"], dtype = np.float32)

    return x,y,z,mass

class Mesh:
    def __init__(self, name):
        self.name = name
        self.lb = None
        self.x = None
        self.y = None
        self.z = None
        self.R = None
        self.phi = None
        self.ax_tot = None
        self.ay_tot = None
        self.ar = None
        self.Vcirc = None
    

        def snapshot_to_grid (nbins = 200):
            """Initializes a mesh in which we are going to calculate accelerations
            This mesh is situated in the plane Z=0, which should correspond with the
            galactic plane if well aligned
            """
            mesh_x = np.zeros(nbins**2, dtype = np.float32)
            mesh_y =  np.zeros(nbins**2, dtype = np.float32)
            mesh_r = np.zeros(nbins**2, dtype = np.float32)
            mesh_z  = np.zeros(nbins**2, dtype = np.float32)
            x_array = y_array = np.linspace(-limit, +limit, nbins)

            m = 0
            #Square mesh, so it is more "uniform" comparing inner and outer radii
            for x in x_array:
                for y in y_array:
                    mesh_x[m],mesh_y[m] = x,y
                    mesh_z[m] = 0
                    mesh_r[m] = np.sqrt(x**2 +y**2)
                    m= m+1

            res = [idx for idx, val in enumerate(mesh_r) if val < limit]  #Radial limit for mesh
            self.x = mesh_x[res]
            self.y = mesh_y[res]
            self.z = mesh_z[res]
            self.R = mesh_r[res]
            self.phi = np.mod(np.arctan2(self.y,self.x), 2*np.pi)

        snapshot_to_grid()


    def calculate_force(self, x_comp, y_comp, z_comp, mass_comp):
        """Divides in threads and calculates forces/accelerations
        """
        pool = Pool(4) #Multiprocessing

        coord = []
        for i,j,k in zip(self.x, self.y, self.z):
            coord.append([i,j,k])
        a = zip(coord,repeat(x_comp, len(self.x)), repeat(y_comp, len(self.x)),
                repeat(z_comp, len(self.x)),repeat(mass_comp, len(self.x)))

        res = pool.starmap(force_in_mesh_gen, a)

        pool.close()
        pool.join()


        ax_tot =  [item[0] for item  in res ] 
        ay_tot =  [item[1] for item  in res ] 

        return ax_tot, ay_tot


    def calculate_vcirc (self):

        snapshot = Snapshot(self.name)
        snapshot.load_stars()
        snapshot.load_dm()
        snapshot.load_gas()

        x_dm, y_dm, z_dm, mass_dm = extract_coord_mass(snapshot.dm) 
        print("Dark matter completed!")

        x_gas, y_gas, z_gas, mass_gas = extract_coord_mass(snapshot.gas)
        print("Gas completed!")
        
        x_stars, y_stars, z_stars, mass_stars = extract_coord_mass(snapshot.stars)
        print("Stars completed!")

        mass_tot = np.concatenate((mass_dm, mass_gas, mass_stars), axis=0)

        #Calculates forces/accelerations in X-Y plane
        dm_ax, dm_ay = self.calculate_force(x_dm, y_dm, z_dm, mass_dm)
        stars_ax, stars_ay = self.calculate_force(x_stars, y_stars, z_stars, mass_stars)  
        gas_ax, gas_ay = self.calculate_force(x_gas, y_gas, z_gas, mass_gas)  

        #Fom X,Y to R
        ar_dm = (self.x*dm_ax + self.y*dm_ay)/self.R
        ar_gas = (self.x*gas_ax + self.y*gas_ay)/self.R
        ar_stars = (self.x*stars_ax + self.y*stars_ay)/self.R

        ar_total = ar_dm + ar_gas + ar_stars
        self.Vcirc = np.sqrt(ar_total*self.R*kpc_to_km)

        #Save total ar and for every component, in case we want to compare
        data ={'X':self.x, 'Y':self.y,  'Z':self.z, 'R':self.R,'Phi':self.phi,'ar_dm':ar_dm, 'a_stars':ar_stars, 
        'ar_gas':ar_gas, 'ar':ar_total, 'Vcirc':np.sqrt(-ar_total*self.R*kpc_to_km)}
    
        mesh_completa = pd.DataFrame(data)
        print(mesh_completa["Vcirc"])

        mesh_completa.to_csv(f"results/Vcirc_mesh_{self.name}_nogauss_components.csv", sep = ",")
            
    def plot_Vcirc (self):

      #  plt.style.use('dark_background')
        size = 5
        ancho = limit + 5
        fig, ax = plt.subplots(1, 1, sharex=False, sharey=True,figsize = (5,4))
        az = ax.scatter(self.x, self.y, marker='s', c=self.Vcirc, 
                    cmap= "rainbow", s = size, vmin =50, vmax = 400)
        #ax.set_title(Snapshot)
        cbar_az_ax = fig.add_axes([0.36, 0.1, 0.01,0.85 ])
        fig.colorbar(az,cbar_az_ax )

        ax.set_xlabel("X [kpc]")
        ax.set_ylabel("Y [kpc]")
        ax.set_xlim(-ancho,ancho)
        ax.set_ylim(-ancho,ancho)

        #plt.subplots_adjust(left=0.125,bottom=0.1, right=0.9, top=0.9, wspace=0.3,hspace=0.35)

        plt.savefig(f"Figures/{self.name}.png", format='png', dpi=150, bbox_inches='tight')

       # gc.collect()



