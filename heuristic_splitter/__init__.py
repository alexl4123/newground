# pylint: disable=E1124
"""
Main Entry Point into the heuristic_splitter.
Parses arguments.
"""

import time
import argparse
import sys

from heuristic_splitter.heuristic_splitter import HeuristicSplitter

from heuristic_splitter.enums.heuristic_strategy import HeuristicStrategy
from heuristic_splitter.enums.grounding_strategy import GroundingStrategy
from heuristic_splitter.enums.sota_grounder import SotaGrounder
from heuristic_splitter.enums.treewidth_computation_strategy import TreewidthComputationStrategy

def main():
    """
    Main Entry Point into the prototype.
    Parses arguments and calls heurstic_splitter class.
    """

    sota_grounder = {
        "GRINGO": {
            "cmd_line":"gringo",
            "enum_mode": SotaGrounder.GRINGO
        },
        "IDLV": {
            "cmd_line":"idlv",
            "enum_mode": SotaGrounder.IDLV
        },
    }

    grounding_strategies = {
        "FULL": {
            "cmd_line": "full",
            "enum_mode": GroundingStrategy.FULL
            },
        "SUGGEST_USAGE": {
            "cmd_line": "suggest-bdg-usage",
            "enum_mode": GroundingStrategy.SUGGEST_USAGE,
        },
    }

    heuristic_methods = {
        "VARIABLE": {
            "cmd_line": "variable",
            "enum_mode": HeuristicStrategy.VARIABLE
            },
        "TREEWIDTH_PURE": {
            "cmd_line": "treewidth-pure",
            "enum_mode": HeuristicStrategy.TREEWIDTH_PURE,
        },
    }


    treewidth_strategies = {
        "NETWORKX": {
            "cmd_line": "networkx",
            "enum_mode": TreewidthComputationStrategy.NETWORKX_HEUR
            },
        "TWALGOR": {
            "cmd_line": "twalgor-exact",
            "enum_mode": TreewidthComputationStrategy.TWALGOR_EXACT,
        },
    }



    parser = argparse.ArgumentParser(prog="heuristic", usage="%(prog)s [files]")
    parser.add_argument(
        "--heuristic-method",
        default=heuristic_methods["TREEWIDTH_PURE"]["cmd_line"],
        choices=[
            heuristic_methods[key]["cmd_line"]
            for key in heuristic_methods.keys()
        ],
    )

    parser.add_argument(
        "--sota-grounder",
        default=sota_grounder["GRINGO"]["cmd_line"],
        choices=[
            sota_grounder[key]["cmd_line"]
            for key in sota_grounder.keys()
        ],
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug information.",
    )

    parser.add_argument(
        "--tw-aware",
        action="store_true",
        help="Use treewidth aware rewritings for rule decomposition (lpopt tool).",
    )

    parser.add_argument(
        "--enable-logging",
        action="store_true",
        help="Write to a file which rules where grounded with BDG, and which with SOTA techniques.",
    )

    parser.add_argument(
        "--logging-file",
        type=str, 
        help="Path to the logging file (--enable-logging must be supported as well). Default a file in logs/<CURRENT-DATE-TIME>.log is generated."
    )




    parser.add_argument(
        "--treewidth-strategy",
        default=treewidth_strategies["NETWORKX"]["cmd_line"],
        choices=[
            treewidth_strategies[key]["cmd_line"]
            for key in treewidth_strategies.keys()
        ],
    )
    parser.add_argument(
        "--grounding-strategy",
        default=grounding_strategies["FULL"]["cmd_line"],
        choices=[
            grounding_strategies[key]["cmd_line"]
            for key in grounding_strategies.keys()
        ],
    )

    parser.add_argument("files", type=argparse.FileType("r"), nargs="+")
    args = parser.parse_args()

    heuristic_method = None
    for key in heuristic_methods.keys():
        if args.heuristic_method == heuristic_methods[key]["cmd_line"]:
            heuristic_method = heuristic_methods[key]["enum_mode"]

    treewidth_strategy = None
    for key in treewidth_strategies.keys():
        if args.treewidth_strategy == treewidth_strategies[key]["cmd_line"]:
            treewidth_strategy = treewidth_strategies[key]["enum_mode"]

    grounding_strategy = None
    for key in grounding_strategies.keys():
        if args.grounding_strategy == grounding_strategies[key]["cmd_line"]:
            grounding_strategy = grounding_strategies[key]["enum_mode"]

    sota_grounder_used = None
    for key in sota_grounder.keys():
        if args.sota_grounder == sota_grounder[key]["cmd_line"]:
            sota_grounder_used = sota_grounder[key]["enum_mode"]



    debug_mode = args.debug
    enable_lpopt = args.tw_aware


    files = args.files
    #files = [open("TEST/190_heur.lp", "r")]
    contents = []
    for f in files:
        contents.append(f.read())
    contents = "\n".join(contents)

    start_time = time.time()
    heuristic = HeuristicSplitter(
        heuristic_method,
        treewidth_strategy,
        grounding_strategy,
        debug_mode,
        enable_lpopt,
        args.enable_logging,
        args.logging_file,
        sota_grounder_used = sota_grounder_used,
    )

    heuristic.start(contents)

    end_time = time.time()
    if debug_mode is True:
        print(f"--> Total elapsed time for generation: {end_time - start_time}")
