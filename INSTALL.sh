#!/usr/bin/env bash
cd#Install
pip install -r requirements.txt || exit
cd gb/static
npm install || exit
bower install || exit
grunt build || exit
cd ../../
python runserver.py || exit
