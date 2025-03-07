APPLICATION_NAME = nagg
CPYTHON_VERSION_1=*
CPYTHON_VERSION_2=*

install:
	python -m pip install .

install-doc:
	python -m pip install .[doc]

install-format:
	python -m pip install .[format]

install-lint-flake8:
	python -m pip install .[lint_flake8]

install-lint-pylint:
	python -m pip install .[lint_pylint]

install-all:
	python -m pip install .[doc,format,lint_flake8,lint_pylint]

uninstall:
	python -m pip uninstall $(APPLICATION_NAME)

compile-nagg-cython:
	-python compile_function_combination_part.py build_ext --inplace
	-cp build/lib.$(CPYTHON_VERSION_1)/generate_function_combination_part.$(CPYTHON_VERSION_2) cython_nagg/cython/
	-python compile_comparison_combination_part.py build_ext --inplace
	-cp build/lib.$(CPYTHON_VERSION_1)/generate_comparison_combination_part.$(CPYTHON_VERSION_2) cython_nagg/cython/
	-python compile_generate_head_guesses.py build_ext --inplace
	-cp build/lib.$(CPYTHON_VERSION_1)/generate_head_guesses_helper_part.$(CPYTHON_VERSION_2) cython_nagg/cython
	-python compile_saturation_justification_helper.py build_ext --inplace
	-cp build/lib.$(CPYTHON_VERSION_1)/generate_saturation_justification_helper_variables_part.$(CPYTHON_VERSION_2) cython_nagg/cython/
	-cd cython_nagg/cython; python compile_cython_helpers.py build_ext --inplace
	-cd cython_nagg/cython; cp build/lib.$(CPYTHON_VERSION_1)/cython_helpers.$(CPYTHON_VERSION_2)  .

compile-heuristic-cython-c:
	-cd heuristic_splitter; gcc -shared -fPIC c_output_redirector.c -o c_output_redirector.so
	-cd heuristic_splitter; python compile_get_facts_cython_file.py build_ext --inplace
	-cd heuristic_splitter; cp build/lib.$(CPYTHON_VERSION_1)/heuristic_splitter/get_facts_cython.$(CPYTHON_VERSION_2) .
	-cd heuristic_splitter/program; python compile_preprocess_smodels_program.py build_ext --inplace
	-cd heuristic_splitter/program; cp build/lib.$(CPYTHON_VERSION_1)/heuristic_splitter/program/preprocess_smodels_program.$(CPYTHON_VERSION_2) .

