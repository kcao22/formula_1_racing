# Imports

import json
import os
import pytest

from api import generic_api, ergast_api

# Instantiate GenericAPI
@pytest.fixture(scope="module")
def generic_api_instance():
    return generic_api.GenericAPI("http://ergast.com")

# Instantiate ErgastAPI
@pytest.fixture(scope="module")
def ergast_api_instance():
    return ergast_api.ErgastAPI()

# Test GenericAPI
def test_generic_api_instantiation(generic_api_instance):
    assert isinstance(generic_api_instance, generic_api.GenericAPI)
    
def test_generic_api_attributes(generic_api_instance):
    assert generic_api_instance.base_url == "http://ergast.com"
    
def test_generic_api_get_is_json(generic_api_instance):
    res = generic_api_instance.get("api/f1/1950/5/results.json")
    assert isinstance(res, dict)
    
def test_generic_api_get_has_content(generic_api_instance):
    res = generic_api_instance.get("api/f1/1950/5/results.json")
    assert bool(res)

# Test ErgastAPI
def test_ergast_api_instantiation(ergast_api_instance):
    assert isinstance(ergast_api_instance, generic_api.GenericAPI)
    
def test_ergast_api_attributes(ergast_api_instance):
    assert ergast_api_instance.base_url == "http://ergast.com"
    
def test_ergast_api_get_historical(ergast_api_instance):
    res = ergast_api_instance.get_historical_race_results(1950, 1950)
    assert isinstance(res, list)
    
def test_ergast_api_get_historical_wrong_range(ergast_api_instance):
    with pytest.raises(expected_exception=ValueError, match="Year range must be between 1950 and current year. Please ensure year start is prior to year end."):
        ergast_api_instance.get_historical_race_results(2020, 2019)

def test_ergast_api_get_historical_before_1950(ergast_api_instance):
    with pytest.raises(expected_exception=ValueError, match="Year range must be between 1950 and current year. Please ensure year start is prior to year end."):
        ergast_api_instance.get_historical_race_results(1930, 2019)
        
def test_ergast_api_get_historical_after_current_year(ergast_api_instance):
    with pytest.raises(expected_exception=ValueError, match="Year range must be between 1950 and current year. Please ensure year start is prior to year end."):
        ergast_api_instance.get_historical_race_results(1950, 2050)
        
def test_ergast_api_get_historical_same_year(ergast_api_instance):
    res = ergast_api_instance.get_historical_race_results(1950, 1950)
    assert len(res) == 1
        
def test_ergast_api_get_historical_different_year(ergast_api_instance):
    res = ergast_api_instance.get_historical_race_results(1950, 1951)
    assert len(res) == 2

def test_ergast_api_get_latest_race_results_is_json(ergast_api_instance):
    res = ergast_api_instance.get_latest_race_results()
    assert isinstance(res, dict)
    
def test_ergast_api_get_latest_race_results_has_content(generic_api_instance):
    res = generic_api_instance.get("api/f1/1950/5/results.json")
    assert bool(res)
    
def test_get_all_data_saves(ergast_api_instance):
    ergast_api_instance.get_all_data("/mnt/d/Documents/Data Projects/formula_1_racing/data")
    list_csv_objs = [file for file in os.listdir("data") if file.endswith('.csv')]
    assert len(list_csv_objs) == 14
