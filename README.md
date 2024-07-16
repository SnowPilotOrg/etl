# Snowpilot Connectors

This repository defines a spec for connectors that do simple data extraction and loading from "streams", meaning a bounded or unbounded dataset in a database, SaaS product, or file.

It also contains some example connectors following the Snowpilot specification.

The Snowpilot Spec is primarily inspired by the [Singer Spec]([url](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md)), but makes a few adjustments
to better allow for data transfer into externally-managed data stores such as SaaS products.

Similarities between the Snowpilot Spec and the Singer Spec:
- Simple message passing over stdin/stdout
- Unix-like API - a one-time ETL job can simply be invoked with the Unix pipe operator. Ex. `csv extract | hubspot load`
- Independent connectors that can be written in any programming language, provided that they obide by the connector specification.

Differences between the Snowpilot Spec and the Singer Spec:
- Discovery of schemas for for extraction and loading (Singer requires discovery only on the extraction side)
- Per-operation schemas, again to account for the sometimes-differing shape of insert/update/upsert APIs found in SaaS products. This approach is inspired by the Typescript type generation done by Supabase.
- No concept of state capture or incremental replication. NOTE: this may change in the future, but this spec is meant to cover only simple cases to begin with.
