import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    print("Rides with zero passengers", data['passenger_count'].isin([0]).sum())
    print("Rides with zero trip distance", data['trip_distance'].isin([0]).sum())

    data = data[data['passenger_count'] > 0] 
    data = data[data['trip_distance'] > 0]
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    print(data['VendorID'].unique())
    print(data.columns)

    new_columns = []
    for column in data.columns:
        new_columns.append(re.sub('([a-z0-9])([A-Z])', r'\1_\2', column).lower())

    data.columns = new_columns
    
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert 'vendor_id' in output.columns
    assert output['passenger_count'].isin([0]).sum() == 0 , 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero trip distance'
