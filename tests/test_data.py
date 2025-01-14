import pytest
import pandas as pd
import os

# Directory where your data is stored
DATA_DIR = "C:/Users/ismac/PycharmProjects/NeuralAgent/utils/prepared_data"  # Adjust this if needed

@pytest.mark.parametrize("file_name", os.listdir(DATA_DIR))
def test_data_files(file_name):
    """
    Test that each CSV file in the data directory can be read
    and contains valid data.
    """
    file_path = os.path.join(DATA_DIR, file_name)
    print(f"Checking {file_name}...")  # For debugging purposes
    try:
        df = pd.read_csv(file_path)
        assert not df.empty, f"{file_name} is empty."
        assert df.shape[1] > 0, f"{file_name} has no columns."
        print(f"{file_name} - Rows: {len(df)}, Columns: {len(df.columns)}")
        print(df.head(5))  # Display the first 5 rows
    except Exception as e:
        pytest.fail(f"Error reading {file_name}: {e}")
