"""Command-line interface for the default ldt default_workflow. The settings
are read from the default config file in user home directory."""
import sys


import ldt
# from ldt.experiments.default_workflow.default_workflow import default_workflow
# from ldt.load_config import config, load_config

if __name__ == "__main__":

    if len(sys.argv) == 1:
        ldt.experiments.default_workflow()
