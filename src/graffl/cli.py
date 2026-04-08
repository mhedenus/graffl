import argparse
import logging
import sys
from importlib import metadata

from rdflib import Graph

from .parser import GrafflParser


def main():
    try:
        __version__ = metadata.version("graffl")
    except metadata.PackageNotFoundError:
        __version__ = "unknown (not installed)"

    arg_parser = argparse.ArgumentParser(
        description="Graffl RDF Parser CLI",
        epilog="Parses a .graffl file and outputs RDF."
    )
    arg_parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Print the program version and exit."
    )
    arg_parser.add_argument(
        "input_file",
        help="Path to the input .graffl file"
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

    # If -v is passed, level is DEBUG. Otherwise, it defaults to WARNING/ERROR (effectively silent).
    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s"
    )

    logger = logging.getLogger(__name__)

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

    if args.output:
        logger.debug(f"Writing output to {args.output}")
        g.serialize(format="turtle", destination=args.output)
    else:
        output = g.serialize(format="turtle")
        print(output)


if __name__ == "__main__":
    main()
