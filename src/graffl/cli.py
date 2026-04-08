import argparse
import logging
import sys
from pathlib import Path

from rdflib import Graph

# Import the global config object and our parser
from .config import CONFIG
from .parser import GrafflParser


def main():
    # 1. Setup argparse
    arg_parser = argparse.ArgumentParser(
        description="Graffl RDF Parser CLI",
        epilog="Parses a .graffl file and outputs RDF N-Triples to stdout."
    )

    arg_parser.add_argument(
        "input_file",
        help="Path to the input .graffl file"
    )

    arg_parser.add_argument(
        "-c", "--config",
        help="Path to an optional config.json file",
        default=None
    )

    arg_parser.add_argument(
        "-o", "--output",
        help="Path to an optional output Turtle file",
        default=None
    )

    arg_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose debug logging"
    )

    args = arg_parser.parse_args()

    # 2. Configure Logging
    # If -v is passed, level is DEBUG. Otherwise, it defaults to WARNING/ERROR (effectively silent).
    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s"
    )

    logger = logging.getLogger(__name__)

    # 3. Load Configuration (if provided via -c)

    if args.config:
        logger.debug(f"Loading configuration from {args.config}")
        CONFIG.load_from_json(args.config)

    # 4. Parse the File
    logger.debug(f"Parsing file: {args.input_file}")

    g = Graph()

    try:
       # rdflib requires an InputSource. We can just open the file and pass the string data.
        with open(args.input_file, 'r', encoding='utf-8') as f:
            data = f.read()

        g.parse(data=data, format="graffl", plugin_parsers={"graffl": GrafflParser})

    except FileNotFoundError:
        logger.error(f"Input file not found: {args.input_file}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred during parsing: {e}")
        sys.exit(1)

    # 5. Output
    if args.output:
        logger.debug(f"Writing output to {args.output}")
        g.serialize(format="turtle", destination=args.output)
    else:
        output = g.serialize(format="turtle")
        print(output)


if __name__ == "__main__":
    main()