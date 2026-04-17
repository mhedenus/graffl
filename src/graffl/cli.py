import argparse
import logging
from importlib import metadata
from pathlib import Path

from rdflib import Dataset

from .parser import parse


def main():
    try:
        __version__ = metadata.version("graffl")
    except metadata.PackageNotFoundError:
        __version__ = "unknown (not installed)"

    arg_parser = argparse.ArgumentParser(
        description="Graffl RDF Parser CLI",
        epilog="Parses a .graffl file and outputs RDF"
    )
    arg_parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Print the program version and exit"
    )
    arg_parser.add_argument(
        "-o", "--output",
        help="Path to an optional output (.trig) file",
        default=None
    )
    arg_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose debug logging"
    )
    arg_parser.add_argument(
        "-d", "--input_dir",
        help="Folder containing .graffl files to parse"
    )
    arg_parser.add_argument(
        "input_files",
        nargs="*",
        help="Path to the input .graffl file(s)"
    )
    args = arg_parser.parse_args()

    # If -v is passed, level is DEBUG. Otherwise, it defaults to WARNING/ERROR (effectively silent).
    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s"
    )

    logger = logging.getLogger(__name__)

    target = Dataset()

    graffl_files = []

    if args.input_dir:
        graffl_files.extend(list(Path(args.input_dir).glob("*.graffl")))

    if args.input_files:
        graffl_files.extend(args.input_files)

    for file in graffl_files:
        logger.debug(f"Parsing file: {file}")
        parse(Path(file), graph=target)

    if args.output:
        logger.debug(f"Writing output to {args.output}")
        target.serialize(format="trig", destination=args.output)
    else:
        output = target.serialize(format="trig")
        print(output)


if __name__ == "__main__":
    main()
