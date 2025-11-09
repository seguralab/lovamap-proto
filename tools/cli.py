#!/usr/bin/env python3
"""
Convert protobuf binary files to JSON format.

This script reads a binary protobuf file generated from the Descriptors.proto
schema and converts it to human-readable JSON format.
"""

import sys
import os
import argparse
from pathlib import Path

try:
    from google.protobuf import json_format
except ImportError:
    print("Error: protobuf package is not installed.", file=sys.stderr)
    print("Install it with: pip install protobuf", file=sys.stderr)
    print("Or install this package with: pipx install lovamap-proto-tools", file=sys.stderr)
    sys.exit(1)

# Try to import the generated protobuf module
try:
    # Look for the generated module in the current working directory
    cwd = Path.cwd()
    if str(cwd) not in sys.path:
        sys.path.insert(0, str(cwd))

    import Descriptors_pb2
except ImportError:
    print("Error: Generated protobuf Python code not found.", file=sys.stderr)
    print("\nYou need to compile the proto file first:", file=sys.stderr)
    print("  protoc --python_out=. src/Descriptors.proto", file=sys.stderr)
    print("\nThis will generate Descriptors_pb2.py in the current directory.", file=sys.stderr)
    print("\nMake sure you run this command from the lovamap-proto directory,", file=sys.stderr)
    print("and run lvmp-pb2json from the same directory.", file=sys.stderr)
    sys.exit(1)


def protobuf_to_json(input_file: str, output_file: str = None, pretty: bool = True) -> None:
    """
    Convert a protobuf binary file to JSON.

    Args:
        input_file: Path to the input protobuf binary file
        output_file: Path to the output JSON file (optional)
        pretty: Whether to pretty-print the JSON (default: True)
    """
    # Read the binary protobuf file
    try:
        with open(input_file, 'rb') as f:
            binary_data = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse the binary data as a Descriptors message
    descriptors = Descriptors_pb2.Descriptors()
    try:
        descriptors.ParseFromString(binary_data)
    except Exception as e:
        print(f"Error parsing protobuf data: {e}", file=sys.stderr)
        print("Make sure the input file is a valid Descriptors protobuf binary.", file=sys.stderr)
        sys.exit(1)

    # Convert to JSON
    try:
        json_data = json_format.MessageToJson(
            descriptors,
            preserving_proto_field_name=True,  # Use original field names from proto
            indent=2 if pretty else None
        )
    except Exception as e:
        print(f"Error converting to JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(json_data)
            print(f"Successfully converted '{input_file}' to '{output_file}'")
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print to stdout
        print(json_data)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Convert protobuf binary files to JSON format.',
        epilog='Example: lvmp-pb2json input.pb output.json'
    )
    parser.add_argument(
        'input_file',
        help='Path to the input protobuf binary file'
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Path to the output JSON file (optional, prints to stdout if not specified)'
    )
    parser.add_argument(
        '--compact',
        action='store_true',
        help='Output compact JSON instead of pretty-printed'
    )

    args = parser.parse_args()

    protobuf_to_json(
        args.input_file,
        args.output_file,
        pretty=not args.compact
    )


if __name__ == '__main__':
    main()
