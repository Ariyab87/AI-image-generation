#!/bin/bash

cd "$(dirname "$0")/.." && pwd

start_sh_server
start_code_server

python3 ./src/ignite.py

infinite_loop