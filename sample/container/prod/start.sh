#!/bin/bash
voila /home/jovyan/japper_app/app.ipynb --Voila.base_url="/user/$JUPYTERHUB_USER/" --enable_nbextensions=True --autoreload=True --no-browser --Voila.ip=0.0.0.0 --Voila.root_dir=/home/jovyan/japper_app --port=8888 --show_tracebacks=True --preheat_kernel=True
