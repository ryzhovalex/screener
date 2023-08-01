import subprocess
import argparse
from loguru import logger

from screener.cli import CLI


def main():
    # read live output stream
    # https://stackoverflow.com/a/18422264

    logger.add("var/app.log", serialize=True, rotation="10 MB")

    CLI().parse().execute()


if __name__ == "__main__":
    main()
