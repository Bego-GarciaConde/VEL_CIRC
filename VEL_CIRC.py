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

from mesh_utils import Mesh
 
for name in snapshots_analysis:
    mesh = Mesh(name)
    mesh.calculate_vcirc()
    mesh.plot_Vcirc()



if __name__ == "__main__":
    main()
