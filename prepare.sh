#!/bin/bash
python3 tools/build.py
cd build
zip -r service.raspberrytv.alexa.sinricpro.zip service.raspberrytv.alexa.sinricpro
cd ..
# scp build/service.raspberrytv.alexa.sinricpro.zip osmc@$1:/home/osmc/

