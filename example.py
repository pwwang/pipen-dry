"""A dry run example"""

import os
import sys
from pipen import Proc, Pipen
from dotenv import load_dotenv

load_dotenv()


class P1(Proc):
    input = "infile:file"
    output = "outfile:file:out.txt"
    script = "sleep 30; echo whatever > {{out.outfile}}"


class P2(P1):
    requires = P1
    output = "outdir:dir:outdir"
    script = "sleep 20; mkdir -p {{out.outdir}};"


if __name__ == "__main__":
    is_cloud = len(sys.argv) > 1 and sys.argv[1] == "--cloud"
    pipeline = (
        Pipen(loglevel="debug", scheduler="dry")
        if not is_cloud
        else Pipen(
            loglevel="debug",
            scheduler="dry",
            workdir=f"gs://{os.environ['BUCKET']}/pipen-dry-example",
        )
    )
    pipeline.set_start(P1).set_data([__file__]).run()
