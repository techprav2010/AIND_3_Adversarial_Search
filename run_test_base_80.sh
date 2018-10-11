#!/usr/bin/env bash

log_prfix="base"
pyfile="run_match_base.py"

rounds_def=10
time_def=75 #150 * 5 # 150/2


dir="reports/${log_prfix}_r${rounds_def}_t${time_def}"
mkdir -p $dir

function  play_games {
    rounds=$1
    opponent=$2
    timems=$3

    log_file="${dir}/${log_prfix}_${opponent}_r${rounds}_t${timems}.txt"
    touch $log_file
    echo "python $pyfile --opponent $opponent -r $rounds -l $log_file -t $timems " ; echo

    python $pyfile --opponent $opponent -r $rounds -l  $log_file -t $timems

    echo "python $pyfile  --opponent $opponent -r $rounds -l $log_file -t $timems " >>  $log_file
    echo  "" >>  $log_file
}

#usage: run_match.py [-h] [-d] [-f] [-r ROUNDS]
#                [-o {RANDOM,GREEDY,MINIMAX,SELF}] [-p PROCESSES]
#                [-t TIME_LIMIT]

#"RANDOM": Agent(RandomPlayer, "Random Agent"),
#"GREEDY": Agent(GreedyPlayer, "Greedy Agent"),
#"MINIMAX": Agent(MinimaxPlayer, "Minimax Agent"),
#"SELF": Agent(CustomPlayer, "Custom TestAgent")

#play_games $rounds_def  'MINIMAX' $time_def


play_games $rounds_def  'RANDOM' $time_def
play_games $rounds_def  'GREEDY' $time_def
play_games $rounds_def  'MINIMAX' $time_def
play_games $rounds_def  'SELF' $time_def

