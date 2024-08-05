from .. import CustomFormatter
from argparse import ArgumentParser
import logging

from src.web.app import app
from src.web.precomp import clean_pages, generate_pages


def main() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.INFO)
    streamhandler.setFormatter(CustomFormatter())
    logger.addHandler(streamhandler)

    parser = ArgumentParser(description="Web app for CourseRekt")
    parser.add_argument("-p", "--port", type=int, default=5000,
                        help="Port where the app is run.")
    parser.add_argument("-s", "--skip-precompute", action="store_true",
                        help="Use existing static pages instead of re-computing them.")
    parser.add_argument("-c", "--clean", action="store_true",
                        help="Cleans prior generated pages prior to running app.")
    args = parser.parse_args()

    if args.clean:
        clean_pages()
    if args.clean and args.skip_precompute:
        logger.warning("Cleaned pages but not rebuilding! Consider not using "
                       "--skip-precompute with --clean!")

    if not args.skip_precompute:
        generate_pages()

    app.run(host="0.0.0.0", port=args.port, debug=True)


if __name__ == "__main__":
    main()
