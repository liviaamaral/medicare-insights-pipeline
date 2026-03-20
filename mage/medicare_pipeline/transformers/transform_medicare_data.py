import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    # rename columns to snake_case
    data.columns = (
        data.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
    )

    # drop rows with null values in key columns
    data = data.dropna(subset=[
        'provider_id',
        'provider_state',
        'average_total_payments'
    ])

    # ensure numeric columns are correct type
    numeric_cols = [
        'total_discharges',
        'average_covered_charges',
        'average_total_payments',
        'average_medicare_payments'
    ]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # add a derived column
    data['out_of_pocket'] = (
        data['average_total_payments'] - data['average_medicare_payments']
    )

    return data


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert len(output) > 0, 'The output is empty'
    assert 'out_of_pocket' in output.columns, 'out_of_pocket column missing'
    assert output['provider_state'].isnull().sum() == 0, 'Null states found'