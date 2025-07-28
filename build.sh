#!/bin/bash

echo "Instaluji závislosti..."
pip install -r requirements.txt

echo "Kompiluji aplikaci do EXE..."
pyinstaller ClusterAnalysis.spec

