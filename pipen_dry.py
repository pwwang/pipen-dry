
"""Dry run a pipeline for pipen"""

from pathlib import Path
from typing import TYPE_CHECKING, Union

from slugify import slugify
from xqute.scheduler import Scheduler
from xqute.defaults import JobStatus
from xqute.utils import a_mkdir
from pipen import plugin
from pipen.scheduler import get_scheduler
from pipen.job import Job
from pipen.defaults import ProcOutputType
from pipen.utils import get_logger

if TYPE_CHECKING:
    from pipen import Proc


__version__ = "0.0.2"

SCHEDULER_NAME = "dry"

logger = get_logger("dry", "info")


class DryJob(Job):
    """The job class for the scheduler"""

    def wrap_cmd(self, scheduler: "Scheduler") -> str:
        """Wrap the command, but we don't need to anything"""
        return ""


class PipenDryScheduler(Scheduler):
    """The dry run scheduler"""

    name = SCHEDULER_NAME
    job_class = DryJob
    version = __version__

    async def job_is_running(self, job: Job) -> bool:
        """Doesn't matter, we don't really submit jobs"""
        return False

    async def kill_job(self, job: Job):
        """We don't need to kill the job"""
        return

    async def submit_job(self, job: Job) -> Union[int, str]:
        """Fake job submission.

        Try to generate the output by types
        """
        Path(job.status_file).write_text(str(JobStatus.FINISHED))
        Path(job.rc_file).write_text("0")
        Path(job.stderr_file).write_text("")
        Path(job.stdout_file).write_text("")

        # generate output
        for key, typ in job._output_types.items():
            if typ == ProcOutputType.FILE:
                Path(job.output[key]).write_text("")
            if typ == ProcOutputType.DIR:
                await a_mkdir(job.output[key], parents=True, exist_ok=True)
        return f"DRY-{job.index}"


class PipenDry:
    """Implement some hooks to modify settings and print information"""

    version = __version__

    @plugin.impl
    def on_proc_init(self, proc: "Proc") -> None:
        """Modify the workdir of the process and set cache/export to False"""
        sched = get_scheduler(
            proc.scheduler or proc.pipeline.config.scheduler
        )

        if sched.name != SCHEDULER_NAME:
            return

        proc.__class__.workdir = (
            Path(proc.pipeline.workdir)
            / f"{slugify(proc.name)}.dry"
        )

        proc.cache = False
        proc.export = False

    @plugin.impl
    async def on_proc_start(self, proc: "Proc") -> None:
        """Indicate the process is running in dry-run mode"""
        if proc.scheduler.name == SCHEDULER_NAME:
            proc.log(
                "warning",
                "[yellow]DRY-RUNNING THIS PROCESS[/yellow].",
                logger=logger
            )
