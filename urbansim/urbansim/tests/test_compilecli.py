"""
Tests of the command line interface for generating model Python files.

"""
import os.path
import shutil
import tempfile

import pytest
import yaml
import simplejson as json

from .. import compilecli

TEST_CONFIG = {
    'growth_rate': 0.05,
    'internalname': 'households',
    'model': 'transitionmodel2',
    'output_varname': 'household_id',
    'table': 'dset.households',
    'zero_out_names': ['building_id']
}


def setup_module(module):
    module.TEST_DIR = tempfile.mkdtemp()


def teardown_module(module):
    shutil.rmtree(module.TEST_DIR)


@pytest.fixture(autouse=True)
def temp_data_dir(monkeypatch):
    monkeypatch.setenv('DATA_HOME', TEST_DIR)


def test_model_save_with_dict():
    compilecli.model_save(TEST_CONFIG)
    assert os.path.exists(os.path.join(TEST_DIR, 'models', 'autorun_run.py'))


def test_model_save_with_file_json():
    test_file = os.path.join(TEST_DIR, 'test_config.json')

    with open(test_file, 'w') as f:
        json.dump(TEST_CONFIG, f)

    compilecli.model_save(test_file)
    assert os.path.exists(
        os.path.join(TEST_DIR, 'models', 'test_config_run.py'))


def test_model_save_with_file_yaml():
    test_file = os.path.join(TEST_DIR, 'test_config.yaml')

    with open(test_file, 'w') as f:
        yaml.dump(
            TEST_CONFIG, f, default_flow_style=False, indent=4, width=50)

    compilecli.model_save(test_file)
    assert os.path.exists(
        os.path.join(TEST_DIR, 'models', 'test_config_run.py'))
