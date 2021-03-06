import numpy as np



class Generator:
    """This Generator class is used to build "n_scenarios" OD matrices generated by exploiting
     statistics (mean and standard deviation) of invented hystorical data:
    1. a minimum and maximum OD matrix "n_stations x n_stations" 
    2. "1095 (3 years)" OD matrices belonging to range [minimum, maximum] representing invented hystorical data
    3. compute the mean and standard deviation over all the generated matrices 
    4. generates "n_scenarios" OD matrices by using a distribution among 3 different distributions:
        Uniform, Normal and Exponential and each trip occurs with a probability that is inversely
        proportional to the distance between stations.
    """
    def __init__(self, n_scenarios=1000, n_stations=22, distr="norm"):
        self.min_od_matrix = np.around(
            np.absolute(np.random.uniform(0, 3, size=(n_stations, n_stations)))
        )
        self.max_od_matrix = np.around(
            np.absolute(np.random.uniform(3, 10, size=(n_stations, n_stations)))
        )

        self.prob_matrix = np.zeros((n_stations, n_stations))

        for i in range(n_stations):
            for j in range(n_stations):
                if i != j:
                    self.prob_matrix[i, j] = i + j
                    self.prob_matrix[i, j] = 1 - (
                        self.prob_matrix[i, j] / ((n_stations - 1) * 2)
                    )
        self.hystory = [np.around(np.random.uniform(self.min_od_matrix, self.max_od_matrix)) for _ in range(1095)]#1095=3years
        self.hystory = np.array(self.hystory)

        # mean equal for all distributions: uniform, exponential and normal
        self.mean_od_matrix = np.around(np.mean(np.array(self.hystory), axis=0))

        #std for normal
        self.std_od_matrix_norm = np.around(np.std(np.array(self.hystory), axis=0))

        #std for exponential
        self.std_od_matrix_expo = self.mean_od_matrix

        

        if distr == "norm":
            self.scenario_arrays = [self.normal_matrix() for _ in range(n_scenarios)]
        elif distr == "uni":
            self.scenario_arrays = [self.uniform_matrix() for _ in range(n_scenarios)]
        elif distr == "expo":
            self.scenario_arrays = [
                self.exponential_matrix() for _ in range(n_scenarios)
            ]
        else:
            raise ValueError(
                "distribution must be one between 'norm', 'uni' and 'expo'"
            )

        self.scenario_res = np.stack(self.scenario_arrays, axis=2)

    def normal_matrix(self):

        return np.floor(
            self.prob_matrix * np.around( np.absolute(np.random.normal(self.mean_od_matrix, self.std_od_matrix_norm)))
        )

    def uniform_matrix(self):
        return np.floor(
            self.prob_matrix * np.around(np.random.uniform(self.min_od_matrix, self.max_od_matrix))
        )

    def exponential_matrix(self):
        return np.floor( self.prob_matrix * np.around(np.random.exponential(self.std_od_matrix_expo))
        )

# if __name__=="__main__":
#     gen = Generator(500,22)
    
    