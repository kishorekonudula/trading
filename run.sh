#!/bin/bash
python update_prices.py
python recommend_sells.py
python recommend_buys.py $1
