import os
import sys
import argparse
import time
import subprocess

import tempfile

import clingo

from newground.newground import Newground
from newground.default_output_printer import DefaultOutputPrinter

from start_benchmark_tests import Benchmark

class CustomOutputPrinter(DefaultOutputPrinter):

    def __init__(self):
        self.current_rule_hashes = {}
        self.string = ""

    def custom_print(self, string):
        string_hash = hash(string)

        if string_hash in self.current_rule_hashes:
            return
        else:
            self.current_rule_hashes[string_hash] = string_hash
            self.string = self.string + str(string) + '\n'

    def get_string(self):
        return self.string

class Context:
    def id(self, x):
        return x

    def seq(self, x, y):
        return [x, y]

class PrimitiveBenchmark:

    def __init__(self):
        self.clingo_output = []
        self.newground_output = []

        self.clingo_hashes = {}
        self.newground_hashes = {}

    def on_model(self, m, output, hashes):
        symbols = m.symbols(shown=True)
        output.append([])
        cur_pos = len(output) - 1
        for symbol in symbols:
            output[cur_pos].append(str(symbol))

        output[cur_pos].sort()

        hashes[(hash(tuple(output[cur_pos])))] = cur_pos

    def parse(self):
        parser = argparse.ArgumentParser(prog='Primitive Benchmark', description='Benchmarks Newground vs. Clingo (total grounding + solving time).')

        parser.add_argument('instance')
        parser.add_argument('encoding')
        args = parser.parse_args()

        instance_filename = args.instance
        encoding_filename = args.encoding

        if not os.path.isfile(instance_filename):
            print(f'Provided instance file \'{instance_filename}\' not found or is not a file')
            return
        if not os.path.isfile(encoding_filename):
            print(f'Provided encoding file \'{encoding_filename}\' not found or is not a file')
            return

        instance_file_contents = open(instance_filename, 'r').read()
        encoding_file_contents = open(encoding_filename, 'r').read()

        return (instance_file_contents, encoding_file_contents)



    def start(self, instance_file_contents, encoding_file_contents, config, verbose = True, one_directional_equivalence = True):

        #gringo_clingo_timeout_occured, gringo_clingo_duration, gringo_duration, gringo_grounding_file_size  = Benchmark.clingo_benchmark(instance_file_contents, encoding_file_contents, config, 1800)
        idlv_clingo_timeout_occured, idlv_clingo_duration, idlv_duration, idlv_grounding_file_size = Benchmark.idlv_benchmark(instance_file_contents, encoding_file_contents, config, 1800)
        newground_idlv_clingo_timeout_occured, newground_idlv_clingo_duration, newground_idlv_duration, newground_idlv_grounding_file_size = Benchmark.newground_benchmark(instance_file_contents, encoding_file_contents, config, 1800, grounder = "IDLV")
        newground_gringo_clingo_timeout_occured, newground_gringo_clingo_duration, newground_gringo_duration, newground_gringo_grounding_file_size = Benchmark.newground_benchmark(instance_file_contents, encoding_file_contents, config, 1800, grounder = "GRINGO")
 
        print(f"[INFO] - <<<<<<<<<<>>>>>>>>>>")
        print(f"[INFO] - Newground-IDLV needed {newground_idlv_clingo_duration} seconds!")
        print(f"[INFO] - Newground-GRINGO needed {newground_gringo_clingo_duration} seconds!")
        #print(f"[INFO] - Clingo needed {gringo_clingo_duration} seconds!")       
        print(f"[INFO] - IDLV needed {idlv_clingo_duration} seconds!")       

        """
        temp_file = tempfile.NamedTemporaryFile()
    
        with open(temp_file.name, "w") as f:
            f.write(instance_file_contents + encoding_file_contents)

        clingo_start_time = time.time()   


        subprocess.run(["./clingo",f"{temp_file.name}"])       

        clingo_end_time = time.time()   
        clingo_duration = clingo_end_time - clingo_start_time
        print(f"[INFO] - Clingo needed {clingo_duration} seconds!")

        no_show = False
        ground_guess = False
        ground = False

        total_content = instance_file_contents + "\n#program rules.\n" + encoding_file_contents

        custom_printer = CustomOutputPrinter()
      
        newground_start_time = time.time()   

        
        newground = Newground(no_show = no_show, ground_guess = ground_guess, ground = ground, output_printer = custom_printer)
        newground.start(total_content)

        newground_end_time = time.time()   
        newground_duration_0 = newground_end_time - newground_start_time
        print(f"[INFO] - Newground duration 0:{newground_duration_0}")

        output_string = custom_printer.get_string()

        temp_file = tempfile.NamedTemporaryFile()
    
        with open(temp_file.name, "w") as f:
            f.write(output_string)

        newground_start_time = time.time()   

        subprocess.run(["./clingo",f"{temp_file.name}"])       

        newground_end_time = time.time()   
        newground_duration_1 = newground_end_time - newground_start_time
        print(f"[INFO] - Newground duration 1:{newground_duration_1}")

        newground_total_duration = newground_duration_0 + newground_duration_1

        print(f"[INFO] - <<<<<<<<<<>>>>>>>>>>")
        print(f"[INFO] - Newground needed {newground_total_duration} seconds!")
        print(f"[INFO] - Clingo needed {clingo_duration} seconds!")
        """


if __name__ == "__main__":

    config = {}
    config["clingo_command"] = "./clingo"
    config["gringo_command"] = "./gringo"
    config["idlv_command"] = "./idlv"
    config["python_command"] = "./python3"

    # Strategies ->  {replace,rewrite,rewrite-no-body}
    config["rewriting_strategy"] = "--aggregate-strategy=rewrite-no-body"
    #config["rewriting_strategy"] = "--aggregate-strategy=rewrite"
    #config["rewriting_strategy"] = "--aggregate-strategy=replace"


    checker = PrimitiveBenchmark()
    (instance, encoding) = checker.parse()
    checker.start(instance, encoding, config, verbose = True)



