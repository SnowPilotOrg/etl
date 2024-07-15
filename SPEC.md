# Snowpilot Connector Specification

## Table of Contents

- [Introduction](#introduction)
- [Connector Modes](#connector-modes)
  - [Discovery Mode](#discovery-mode)
  - [Extract Mode](#extract-mode)
  - [Load Mode](#load-mode)
- [JSON Output Format](#json-output-format)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Security Considerations](#security-considerations)
- [Glossary](#glossary)

## Introduction

The Snowpilot Connector Specification defines a standardized method for discovering available data streams, performing full data extraction, and loading data into destinations. This document outlines the requirements and interface for Snowpilot connectors, focusing on manual selection of data streams and full extraction processes. It provides guidelines for implementing connectors that can efficiently discover, extract, and load data in various scenarios.

This specification is inspired by the Singer project but is an independent and incompatible standard. It aims to provide a flexible and efficient way to programmatically retrieve metadata about available streams, extract data, and load data into destinations, without the need to run separate extractor and loader processes.

Connectors are designed to operate in three modes based on the provided command-line arguments:

1. `discover`: Outputs metadata describing the streams and relationships it knows about.
2. `extract`: Acts as an extractor, producing schema and record messages.
3. `load --operation=[OPERATION]`: Acts as a loader, consuming schema and record messages, performing operations based on the specified `[OPERATION]` argument (create, update, upsert, or delete).

These modes enable a unified approach to data integration, allowing for seamless discovery, extraction, and loading of data across various systems and platforms.

## Connector Modes

### Discovery Mode

Discovery mode is invoked using the `discover` command:

snowpilot discover --config config.json

In this mode, the connector outputs metadata about streams and relationships it knows about, including schemas for create, update, upsert, and delete operations.

### Extract Mode

Extract mode is invoked using the `extract` command:

snowpilot extract --config=config.json --stream=<stream_id> --fields=id,email,name

In this mode, the connector acts as an extractor, producing schema and record messages. The `--stream` flag specifies the stream ID to extract from, and the `--fields` flag allows for a comma-separated list of fields to extract.

### Load Mode

Load mode is invoked using the `load` command-line argument along with `--stream`, `--operation`, and `--fields` arguments:

snowpilot load --config=config.json --stream=<stream_id> --operation=<operation_name> --fields=email,firstname,lastname

In this mode, the connector acts as a loader, consuming schema and record messages. It performs operations based on the specified `<operation_name>` argument (e.g., insert, update, upsert) for the specified `<stream_id>`, focusing on the fields listed in the `--fields` argument.

## JSON Output Format

The JSON output for the discovery mode follows the Snowpilot Connector format, which includes schemas of available streams, their properties, and separate schemas for different operations. An example of the output is as follows:

{
"streams": [
{
"id": "users",
"name": "Users",
"schema": {
"row": {
"type": "object",
"properties": {
"id": {"type": "integer"},
"name": {"type": "string"},
"email": {"type": "string", "format": "email"},
"created_at": {"type": "string", "format": "date-time"}
},
"required": ["id"]
},
"insert": {
"type": "object",
"properties": {
"name": {"type": "string"},
"email": {"type": "string", "format": "email"}
},
"required": ["name", "email"]
},
"update": {
"type": "object",
"properties": {
"id": {"type": "integer"},
"name": {"type": "string"},
"email": {"type": "string", "format": "email"}
},
"required": ["id"]
},
"upsert": {
"type": "object",
"properties": {
"id": {"type": "integer"},
"name": {"type": "string"},
"email": {"type": "string", "format": "email"}
},
"required": ["name", "email"]
},
"delete": {
"type": "object",
"properties": {
"id": {"type": "integer"}
},
"required": ["id"]
}
},
"relationships": [
{
"foreign_key_name": "user_orders",
"columns": ["id"],
"is_one_to_one": false,
"referenced_stream": "orders",
"referenced_columns": ["user_id"]
}
]
}
]
}

Snowpilot Connectors operate in three distinct modes, each invoked by a specific command-line argument:

### 1. Discovery Mode

When invoked with the `discover` command, the connector outputs metadata describing the streams and relationships it knows about. This includes:

- Schemas for row, insert, update, upsert, and delete operations
- Relationships between streams

Example usage:

```shell
snowpilot discover --config config.json > catalog.json
```

### 2. Extract Mode

In extract mode, the connector acts as a data source, performing full extraction and producing:

- Schema messages
- Record messages

Example usage:

```shell
snowpilot extract --config config.json --stream=<stream_id> --fields=id,email,name
```

The `--stream` flag specifies the stream ID to extract from, and the `--fields` flag provides a comma-separated list of fields to extract.

### 3. Load Mode

When used as a loader, the connector consumes:

- Schema messages
- Record messages

It then performs the specified operation (insert, update, upsert, or delete) based on the `--operation` argument, focusing on full loading processes.

Example usage:

```shell
snowpilot load --config config.json --stream=<stream_id> --operation=<operation_name> --fields=email,firstname,lastname
```

The `--stream` flag specifies the stream ID to load to, `--operation` specifies the operation type (e.g., insert, update, upsert), and `--fields` provides a comma-separated list of fields to load.

### Supported Operations and Schema Structure

The discovery output includes separate schemas for different operations within the `schema` object. This information helps in determining the appropriate sync behavior and data structure for each stream. The following operation-specific schemas are used:

- `row`: Schema for read operations, representing the full structure of a record.
- `insert`: Schema for create operations, specifying fields required or allowed when creating new records.
- `update`: Schema for update operations, defining fields that can be modified in existing records.
- `upsert`: Schema combining insert and update operations, used for upserting records.
- `delete`: Schema for delete operations, typically containing key fields to identify records for deletion.

The presence of these operation-specific schemas implies support for the corresponding operations. For example, if an `insert` schema is provided for a stream, it indicates that the stream supports creating new records.

These operation-specific schemas allow for fine-grained control over the sync process, enabling the distinction between different operation types and their corresponding data structures. By providing separate schemas for each operation, the connector can accurately represent the required and optional fields for each action, improving data integrity and reducing errors during the sync process.

### Usage Examples

1. Discovery Mode:

```shell
snowpilot discover > catalog.json
```

2. Extract Mode:

```shell
snowpilot extract --config config.json --stream=contacts --fields=id,email,name
```

3. Load Mode:

```shell
snowpilot load --config config.json --stream=contacts --operation=upsert --fields=email,firstname,lastname
```

These examples demonstrate the command structures for discovery, extract, and load operations in the Snowpilot Connector specification, including the specification of streams, fields, and operations.

The `relationships` field can be used to understand and maintain referential integrity between streams during the sync process. For example, when syncing related data, ensure that the referenced records are created or updated before the referring records.

This structure allows for precise control over how data is written to and read from the source or target system, taking into account the specific requirements of each operation type and the relationships between streams.

## Error Handling

When implementing the discovery mode, developers should consider the following error scenarios and handle them appropriately:

1. Invalid or malformed JSON output
2. Missing required fields in the discovery output
3. Unsupported schema versions
4. Errors in accessing the data source or destination during discovery

Proper error messages should be logged, and the application should gracefully handle these scenarios without crashing.

## Security Considerations

While the discovery mode is typically invoked locally, developers should still consider security measures:

1. Ensure that sensitive configuration information is not exposed in the discovery output
2. Implement proper access controls to ensure that only authorized users can invoke discovery mode
3. Be cautious about revealing too much information about the underlying data structure in the discovery output

## Usage Examples

### Discovering Streams from a Tap

import subprocess
import json

def discover_streams(snowpilot_command, config_file):
result = subprocess.run([snowpilot_command, 'discover', '--config', config_file],
capture_output=True, text=True)
if result.returncode != 0:
raise Exception(f"Discovery failed: {result.stderr}")

    return json.loads(result.stdout)

streams = discover_streams('snowpilot', 'config.json')
print(json.dumps(streams, indent=2))

### Discovering Sinks from a Target

```python
import subprocess
import json

def discover_sinks(target_command, config_file):
    result = subprocess.run([target_command, '--config', config_file, '--discover'],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Discovery failed: {result.stderr}")

    return json.loads(result.stdout)

sinks = discover_sinks('target-example', 'target_config.json')
print(json.dumps(sinks, indent=2))
```

## Glossary

- **snowpilot_connector**: A component that can act as both a source and a destination for data, supporting discovery, extraction, and loading operations.
- **stream**: A collection of data, typically representing a table or API endpoint.
- **discovery_mode**: A feature of connectors that allows programmatic discovery of available streams and their properties.
- **json_schema**: A vocabulary that allows you to annotate and validate JSON documents.
- **create**: An operation that allows for the creation of new records.
- **update**: An operation that allows for updating existing records.
- **upsert**: An operation that updates a record if it exists, or creates a new record if it doesn't exist.
- **delete**: An operation that removes existing records.
- **row**: A schema representing the structure of data for read operations.
- **insert**: A schema defining the structure for creating new records.
- **relationships**: Information describing how streams are related to each other, including foreign key constraints and cardinality.
- **id**: A unique identifier for a data stream, used for programmatic reference and to unambiguously identify streams across the system.
- **name**: A human-readable name for a data stream, suitable for display in user interfaces or reports.
- **operation_schemas**: Specific schemas for different operations (row, insert, update, upsert, delete) within a stream.
- **discover**: Subcommand for invoking the discovery mode of a Snowpilot connector (e.g., `snowpilot discover`).
- **extract**: Subcommand for running a Snowpilot connector in extract (source) mode (e.g., `snowpilot extract --config config.json --stream=<stream_id> --fields=id,email,name`).
- **load**: Subcommand for running a Snowpilot connector in load (destination) mode (e.g., `snowpilot load --config config.json --stream=<stream_id> --operation=<operation_name> --fields=email,firstname,lastname`).
- **--stream**: Flag used to specify the stream ID to extract from or load to.
- **--fields**: Flag used to specify a comma-separated list of fields to extract or load.
- **--operation**: Flag used in load mode to specify the operation type (e.g., insert, update, upsert).
