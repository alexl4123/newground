
import io
import os
import subprocess

from datetime import datetime

from clingo.ast import ProgramBuilder, parse_string

from heuristic_splitter.graph_creator_transformer import GraphCreatorTransformer
from heuristic_splitter.graph_data_structure import GraphDataStructure
from heuristic_splitter.graph_analyzer import GraphAnalyzer

from heuristic_splitter.heuristic_transformer import HeuristicTransformer

from heuristic_splitter.enums.heuristic_strategy import HeuristicStrategy
from heuristic_splitter.enums.treewidth_computation_strategy import TreewidthComputationStrategy
from heuristic_splitter.enums.grounding_strategy import GroundingStrategy
from heuristic_splitter.enums.sota_grounder import SotaGrounder

from heuristic_splitter.heuristic_0 import Heuristic0

from heuristic_splitter.grounding_strategy_generator import GroundingStrategyGenerator
from heuristic_splitter.grounding_strategy_handler import GroundingStrategyHandler

#from heuristic_splitter.get_facts import GetFacts
#from heuristic_splitter.setup_get_facts_cython import get_facts_from_file_handle
from heuristic_splitter.get_facts_cython import get_facts_from_file_handle

class HeuristicSplitter:

    def __init__(self, heuristic_strategy: HeuristicStrategy, treewidth_strategy: TreewidthComputationStrategy, grounding_strategy:GroundingStrategy, 
        debug_mode, enable_lpopt,
        enable_logging = False, logging_file = None,
        output_printer = None, sota_grounder_used = SotaGrounder.GRINGO):

        self.heuristic_strategy = heuristic_strategy
        self.treewidth_strategy = treewidth_strategy
        self.grounding_strategy = grounding_strategy
        self.sota_grounder = sota_grounder_used

        self.debug_mode = debug_mode
        self.enable_lpopt = enable_lpopt
        self.output_printer = output_printer

        self.enable_logging = enable_logging
        path = None
        if self.enable_logging is True and logging_file is None:
            from pathlib import Path
            # Set default logging file:
            current_datetime = datetime.now()
            path_list = ["logs", current_datetime.strftime("%Y%m%d-%H%M%S") + ".log"]
            path = Path(*path_list)
        elif self.enable_logging is True:
            from pathlib import Path
            path = Path(logging_file)

        if path is not None: 
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w") as initial_overwrite:
                initial_overwrite.write("")

            self.logging_file = open(path, "a")
        else:
            self.logging_file = None

    def start(self, contents):

        virtual_file = io.BytesIO(contents.encode("utf-8"))

        try:
            bdg_rules = {}
            sota_rules = {}
            stratified_rules = {}
            lpopt_rules = {}

            constraint_rules = {}
            grounding_strategy = []
            graph_ds = GraphDataStructure()
            rule_dictionary = {}

            # Separate facts from other rules:
            #facts, facts_heads, other_rules, all_heads = GetFacts().get_facts_from_contents(contents)
            facts, facts_heads, other_rules, query = get_facts_from_file_handle(virtual_file)

            all_heads = facts_heads.copy()

            for fact_head in facts_heads.keys():
                graph_ds.add_vertex(fact_head)

            other_rules_string = "\n".join(other_rules)

            # Remove '#program' rules
            other_rules = [string_rule for string_rule in other_rules if not (string_rule.strip()).startswith("#program")]

            graph_transformer = GraphCreatorTransformer(graph_ds, rule_dictionary, other_rules, self.debug_mode)
            parse_string(other_rules_string, lambda stm: graph_transformer(stm))

            graph_analyzer = GraphAnalyzer(graph_ds)
            graph_analyzer.start()

            if self.heuristic_strategy == HeuristicStrategy.TREEWIDTH_PURE:
                heuristic = Heuristic0(self.treewidth_strategy, rule_dictionary, self.sota_grounder, self.enable_lpopt)
            else:
                raise NotImplementedError()

            heuristic_transformer = HeuristicTransformer(graph_ds, heuristic, bdg_rules,
                sota_rules, stratified_rules, lpopt_rules, constraint_rules, all_heads,
                self.debug_mode, rule_dictionary)
            parse_string(other_rules_string, lambda stm: heuristic_transformer(stm))

            generator_grounding_strategy = GroundingStrategyGenerator(graph_ds, bdg_rules, sota_rules,
                stratified_rules, constraint_rules, lpopt_rules, rule_dictionary)
            generator_grounding_strategy.generate_grounding_strategy(grounding_strategy)


            if self.debug_mode is True:
                print(">>>>> GROUNDING STRATEGY:")
                print(grounding_strategy)
                print("<<<<")

            if self.grounding_strategy == GroundingStrategy.FULL:

                grounding_handler = GroundingStrategyHandler(grounding_strategy, rule_dictionary, graph_ds,
                    facts,
                    query,
                    self.debug_mode, self.enable_lpopt,
                    output_printer = self.output_printer, sota_grounder = self.sota_grounder,
                    enable_logging = self.enable_logging, logging_file = self.logging_file,)
                if len(grounding_strategy) > 1 or len(grounding_strategy[0]["bdg"]) > 0:
                    grounding_handler.ground()
                    grounding_handler.output_grounded_program(all_heads)
                else:
                    grounding_handler.single_ground_call(all_heads)

            else:

                facts_string = "\n".join(list(facts.keys()))
                print(facts_string)

                for sota_rule in sota_rules.keys():
                    print(str(rule_dictionary[sota_rule]))

                for strat_rule in stratified_rules.keys():
                    print(str(rule_dictionary[strat_rule]))

                if len(list(bdg_rules.keys())) > 0:
                    print("#program rules.")

                    for bdg_rule in bdg_rules.keys():
                        print(str(rule_dictionary[bdg_rule]))

                if len(query.keys()) > 0:
                    print(list(query.keys())[0])

            if self.logging_file is not None:
                self.logging_file.close()

        except Exception as ex:

            if self.logging_file is not None:
                self.logging_file.close()

            raise ex
