# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 17:06:09 2021

@author: Francesco Conforte
"""
import numpy as np
import random

random.seed(42)

class Generator():
    """This Generator class is used to build "n_scenarios" OD matrices by generating:
    1. a minimum and maximum OD matrix "n_stations x n_stations" 
    2. "n_scenarios" OD matrices belonging to range [minimum, maximum]
    3. compute the mean and standard deviation over all the generated matrices 
    4. generates "n_scenarios" OD matrices by using a monte carlo sampling according to 3 different distributions:
        Uniform, Normal and Exponential.
    """
    def __init__(self, n_scenarios = 1000, n_stations = 22, distr = 'norm'):
        self.min_od_matrix = np.around(np.absolute(np.random.uniform(
                    0,3,
                    size=(n_stations, n_stations))
                ))
        self.max_od_matrix = np.around(np.absolute(np.random.uniform(
                    10, 15,
                    size=(n_stations, n_stations))
                ))

        self.scenarios = [np.around(np.random.uniform(self.min_od_matrix, self.max_od_matrix)) for i in range(n_scenarios)]
        self.scenarios = np.array(self.scenarios)
        
        self.mean_od_matrix = np.around(np.mean(self.scenarios, axis=0))
        self.std_od_matrix = np.around(np.std(self.scenarios, axis=0))

        self.func_list = [self.normal_matrix(), self.uniform_matrix(), self.exponential_matrix()]

        
        self.scenario_arrays = [self.func_list[random.randint(0,2)] for _ in range(n_scenarios)]

        
        self.scenario_res = np.stack(self.scenario_arrays, axis=2)

    def normal_matrix(self):
        return np.around(np.absolute(np.random.normal(self.mean_od_matrix, self.std_od_matrix )))

    def uniform_matrix(self):
        return np.around(np.random.uniform(self.min_od_matrix, self.max_od_matrix))

    def exponential_matrix(self):
        return np.around(np.random.exponential(self.mean_od_matrix))
