import pytest
import os
import pandas as pd

"""
Test Staged csv of : /data/staging/southeast-foraging-clean_IM.csv
"""

back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
path = os.path.join(back_dir,'data','staging','southeast-foraging-clean_IM.csv')
df = pd.read_csv(path)

def test_indicator_matrix_zeros():
    # Uses columns starting from third position
    assert ~( df.iloc[:,2:].eq(0).all().all() ) == True
