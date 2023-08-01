import subprocess
from typing import IO
import typing

from loguru import logger


class Executor:
    """
    Executes different stream reading actions.

    @abstract
    """
    def __init__(
        self,
        *,
        verbose_count: int
    ) -> None:
        self._verbose_count: int = verbose_count

    def execute(self) -> None:
        raise NotImplementedError()


class TailExecutor(Executor):
    pass


class DockerLogsExecutor(Executor):
    def __init__(
        self,
        *,
        container_name: str,
        verbose_count: int
    ) -> None:
        super().__init__(verbose_count=verbose_count)

        self._container_name = container_name

    def execute(self) -> None:
        # use `-n 1` to ensure only new log lines are passed to the executor
        command: str = f"docker logs -f -n 1 {self._container_name}"

        while True:
            process: subprocess.Popen[bytes] = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                shell=True
            )
            process_stdout: IO[bytes] | None = process.stdout

            if process_stdout is None:
                raise ValueError("process stdout is None")
            else:
                # TODO(ryzhovalex): this is temporary solution to check Java
                #   data leaks
                # 0

                for line_bytes in iter(
                    lambda: typing.cast(IO[bytes], process_stdout).readline(),
                    b""
                ):
                    line: str = line_bytes.decode()
                    logger.info(f"[screener] receive line <{line.strip()}>")
                    if "java.lang.OutOfMemory" in line:
                        logger.warning(
                            "[screener] Found Java OutOfMemory exception,"
                            " restarting"
                        )
                        subprocess.run(
                            "docker-compose down && docker-compose up -d",
                            shell=True
                        )
