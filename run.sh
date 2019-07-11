#!/usr/bin/env bash
rm -rf out/*
rm -rf val/*
rm -rf test/*
python ./run.py -l pass2 \
                -e png \
                -b 1 \
                -na 2 \
                -f 50 \
                -c 1 \
                -al 0 \
                -t 4 

python ./run.py -l pass \
                -e png \
                -b 1 \
                -na 2 \
                -f 50 \
                -c 1 \
                -al 0 \
                -t 4 \
                -d 3