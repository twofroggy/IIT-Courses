#!/bin/bash

mode=(flops matrix)
type=(single double)
size=(small medium large)
threads=(1 2 4)

for mode in ${mode[@]}; do 
    for type in ${type[@]}; do 
        for size in  ${size[@]}; do 
            for threads in  ${threads[@]}; do 
                ./cpubench.c ${mode} ${type} ${size} ${threads}
            done
        done
    done
done
