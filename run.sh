#!/usr/bin/env bash
rm -rf out/*
rm -rf val/*
rm -rf test/*
python ./run.py -l pass \
                -e png \
                -b 1 \
                -na 2 \
                -f 50 \
                -c 60 \
                -al 0 \
                -t 3
rm out/labels.txt