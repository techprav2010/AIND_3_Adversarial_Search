#!/usr/bin/env bash

./run_test_advanced.sh > log_advanced_150.log & disown
./run_test_advanced_80.sh > log_advanced_80.log & disown
#./run_test_advanced_700.sh > log_advanced_700.log & disown

./run_test_base.sh > log_base_150.log & disown
./run_test_base_80.sh > log_based_80.log & disown
#./run_test_base_700.sh > log_base_700.log & disown
