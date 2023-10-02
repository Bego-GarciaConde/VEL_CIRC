import numpy as np
import pandas as pd
import gc
from multiprocessing import Pool
from config import *

import sys
sys.path.append('../')

from mesh import Mesh
 
for name in snapshots_analysis:
    mesh = Mesh(name)
    mesh.calculate_vcirc()
    mesh.plot_Vcirc()



if __name__ == "__main__":
    main()
