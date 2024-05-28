#!/bin/bash

# for dev. remove later
pip install -e /home/jovyan/japper

voila ./japper_app/app.ipynb --autoreload=True --no-browser --Voila.ip=0.0.0.0 --Voila.root_dir=/home/jovyan/japper_app --port=8888 --debug  --show_tracebacks=True&
jupyter lab --allow-root --no-browser --ip=0.0.0.0 --port=8889 --IdentityProvider.token='' --ServerApp.password=''