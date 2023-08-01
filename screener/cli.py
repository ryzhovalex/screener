import argparse
from screener.executor import DockerLogsExecutor, Executor, TailExecutor

from screener.sourcetype import SourceType
from screener.utils.never import never

class CLI:
    def parse(self) -> Executor:

        source_type_help: str = """\
        Source's type to listen from. Different
        Source Types support different following arguments.
        """

        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Starts listening to a stream."
        )

        parser.add_argument(
            "-v",
            "--verbose",
            default=0,
            action="count",
            help="Verbosity level.",
            dest="verbose_count"
        )

        subparsers: argparse._SubParsersAction = parser.add_subparsers(
            help=source_type_help,
            dest="source_type"
        )

        tail_type_parser: argparse.ArgumentParser = subparsers.add_parser(
            "tail",
            help="Standard UNIX tail command in following mode.",
        )
        tail_type_parser.add_argument(
            "source",
            type=str,
            help="Where to read from."
        )

        dockerlogs_type_parser: argparse.ArgumentParser = subparsers.add_parser(
            "dockerlogs",
            help="Docker logs of a chosen container.",
        )
        dockerlogs_type_parser.add_argument(
            "container_name",
            type=str,
            help="Name of the container to read logs from."
        )

        return self._get_executor(parser.parse_args())

    def _get_executor(self, args: argparse.Namespace) -> Executor:
        source_type: SourceType = SourceType(args.source_type)

        match source_type:
            case SourceType.Tail:
                return self._get_tail_executor(args)
            case SourceType.DockerLogs:
                return self._get_dockerlogs_executor(args)
            case _:
                never(source_type)

    def _get_tail_executor(self, args: argparse.Namespace) -> TailExecutor:
        raise NotImplementedError

    def _get_dockerlogs_executor(
        self,
        args: argparse.Namespace
    ) -> DockerLogsExecutor:
        return DockerLogsExecutor(
            container_name=args.container_name,
            verbose_count=args.verbose_count
        )
