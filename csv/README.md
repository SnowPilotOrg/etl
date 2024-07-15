# CSV Connector

This project contains the CSV connector, which follows the Snowpilot Connector specification.

## Assumptions

The CSV connector makes the following assumptions about the CSV files it processes:

- The CSV files are encoded in UTF-8.
- Lines in the CSV files are separated by LF (Line Feed) newlines.

Please ensure that your CSV files conform to these assumptions for proper operation of the connector.

## Running Tests

To run the tests for this CSV connector, follow these steps:

1. Ensure you have Poetry installed. If not, install it using:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Navigate to the CSV connector directory:
   ```
   cd connectors/csv
   ```

3. Install the project dependencies using Poetry:
   ```
   poetry install
   ```

4. Run the tests using pytest:
   ```
   poetry run pytest
   ```

This will execute all the tests in the `tests/test_csv_connector.py` file. The output will show you which tests passed or failed, along with any error messages for failed tests.