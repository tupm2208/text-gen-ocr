#!/usr/bin/env bash
rm -rf /home/ai-team/projects/tupm/numberic/out/*
# rm -rf /home/ai-team/projects/tupm/character/val/*
rm -rf test/*

python ./run.py -l pass \
                -e png \
                -b 1 \
                -na 2 \
                -f 50 \
                -c 1 \
                -al 0 \
                -t 4 \
                -d 3 \
                --output_dir /home/ai-team/projects/tupm/numberic/out