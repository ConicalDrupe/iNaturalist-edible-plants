import pytest
import os
import pandas as pd

"""
Test Staged csv of : /data/staging/southeast-foraging-clean_1.csv
"""

back_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
path = os.path.join(back_dir,'data','staging','southeast-foraging-clean_1.csv')
df = pd.read_csv(path)


def test_col_edible_whitespace():
    assert df[df['Common Name'].str.count(' ')>2].any() == None

def test_trailing_whitespace():
    pass

