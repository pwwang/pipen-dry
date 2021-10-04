"""A dry run example"""

from pipen import Proc, Pipen

class P1(Proc):
    input = "infile:file"
    output = "outfile:file:out.txt"
    script = "sleep 3; echo whatever > {{out.outfile}}"

class P2(P1):
    requires = P1
    # If we have typo, dry-running can detect it real quick
    # input_data = lambda ch: [ch.iloc[0,0] + "1"]

if __name__ == "__main__":
    Pipen(
        loglevel="debug",
        scheduler="dry"
    ).set_start(P1).set_data([__file__]).run()
