#!/bin/bash
python3 tools/build.py
cd build
zip -r service.kodi.alexa.tv.zip service.kodi.alexa.tv
cd ..

