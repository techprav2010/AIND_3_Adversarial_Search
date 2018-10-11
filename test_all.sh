#!/usr/bin/env bash

export DEPTH=3; ./run_test_6.sh > log_advanced_d_3.log
export DEPTH=6; ./run_test_6.sh > log_advanced_d_6.log
export DEPTH=9; ./run_test_6.sh > log_advanced_d_9.log
export DEPTH=12; ./run_test_6.sh > log_advanced_d_12.log
export DEPTH=15; ./run_test_6.sh > log_advanced_d_15.log