#!/bin/bash

current_dir=$(pwd)

echo "$current_dir"

echo "export PATH=$PATH:$current_dir" >> ~/.bashrc
