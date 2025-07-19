import os
import pandas as pd
import pytest

cleaned_search_service_output = "gbif_species_match_638_clean.csv"

@pytest.fixture
def df():
    csv_path = os.path.join('/home/boon/Projects/iNaturalist-edible-plants/outputs',cleaned_search_service_output)
    return pd.read_csv(csv_path)

def test_ranks(df):
    assert all(df['rank'].isin(['GENUS','SPECIES']))
    return
