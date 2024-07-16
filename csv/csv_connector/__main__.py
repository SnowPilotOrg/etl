import argparse
from csv_connector import discover, extract, load, parse_config

def main():
    parser = argparse.ArgumentParser(description="CSV Connector for Snowpilot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Discover subcommand
    discover_parser = subparsers.add_parser("discover", help="Discover available streams")
    discover_parser.add_argument("--config", required=True, help="Path to the configuration file")

    # Extract subcommand
    extract_parser = subparsers.add_parser("extract", help="Extract data from CSV files")
    extract_parser.add_argument("--config", required=True, help="Path to the configuration file")

    # Load subcommand
    load_parser = subparsers.add_parser("load", help="Load data into CSV files")
    load_parser.add_argument("--config", required=True, help="Path to the configuration file")

    args = parser.parse_args()

    config = parse_config(args.config)

    if args.command == "discover":
        discover(config)
    elif args.command == "extract":
        extract(config)
    elif args.command == "load":
        load(config)

if __name__ == "__main__":
    main()