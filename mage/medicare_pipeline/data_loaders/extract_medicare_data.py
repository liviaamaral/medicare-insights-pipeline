from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from os import path
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_big_query(*args, **kwargs):
    query = """
        SELECT
            drg_definition,
            provider_id,
            provider_name,
            provider_street_address,
            provider_city,
            provider_state,
            provider_zipcode,
            hospital_referral_region_description,
            total_discharges,
            average_covered_charges,
            average_total_payments,
            average_medicare_payments
        FROM `bigquery-public-data.cms_medicare.inpatient_charges_2015`
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    return BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert len(output) > 0, 'The output is empty'