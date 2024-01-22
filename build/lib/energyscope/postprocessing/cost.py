import pandas as pd
import os
from pathlib import Path


def get_total_cost(config):
    """Read the cost breakdown and computes the total cost

        Parameters
        ----------
        config: dictionnary
        Dictionnary defining the case study

        case: str
        Set to 'deter' for determinist run and 'uq' for uncertainty quatification run

        Returns
        -------
        Total annualised cost of the system (float) [M€/y]
        """
    two_up = Path(__file__).parents[2]

    costs = pd.read_csv(os.path.join(two_up,'case_studies',config['case_study'],'output','cost_breakdown.txt'), index_col=0, sep='\t')
   
    return costs.sum().sum()
