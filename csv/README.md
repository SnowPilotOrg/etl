# CSV Connector

This project contains the CSV connector, which follows the Snowpilot Connector specification.

## Assumptions

The CSV connector makes the following assumptions about the CSV files it processes:

- The CSV files are encoded in UTF-8.
- Lines in the CSV files are separated by LF (Line Feed) newlines.

Please ensure that your CSV files conform to these assumptions for proper operation of the connector.

## Usage

The CSV connector supports three main commands: `discover`, `extract`, and `load`. Each command requires a configuration file to be specified.

### Configuration File

Create a JSON or JSONC (JSON with Comments) configuration file (e.g., `config.json`) with the following structure:

```json
{
  "csv_path": "/path/to/your/csv/file/or/directory"
}
```

### Discover Command

To list available streams and their schemas:

```
python -m csv_connector discover --config config.json
```

### Extract Command

To extract data from a specific stream:

```
python -m csv_connector extract --config config.json
```

### Load Command

To load data into a specific stream:

```
python -m csv_connector load --config config.json
```

## Using Poetry Scripts

This project uses Poetry for dependency management and packaging. Poetry scripts have been set up to make running the CSV connector commands easier.

### Setup

1. Ensure you have Poetry installed. If not, install it following the instructions at https://python-poetry.org/docs/#installation

2. Install the project dependencies:
   ```
   poetry install
   ```

### Running Commands

You can now use the following Poetry scripts to run the CSV connector commands:

1. Discover Command:
   ```
   poetry run discover --config config.json
   ```

2. Extract Command:
   ```
   poetry run extract --config config.json
   ```

3. Load Command:
   ```
   poetry run load --config config.json
   ```

Replace `config.json` with the path to your configuration file.

Note: The configuration file now supports JSONC (JSON with Comments) format.

## Examples

1. Discover available streams:
   ```
   poetry run discover --config /path/to/config.json
   ```

2. Extract data from a stream:
   ```
   poetry run extract --config /path/to/config.json
   ```

3. Load data into a stream:
   ```
   poetry run load --config /path/to/config.json
   ```

Note: Make sure to replace `/path/to/config.json` with the actual path to your configuration file.

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