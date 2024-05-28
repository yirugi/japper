#!/bin/bash

# set the base url for voila
# if JUPYTERHUB_USER is not set, then we are in single user mode
if [[ -z "${JUPYTERHUB_USER}" ]]; then
  VOILA_BASE_URL="/" # for single server mode
else
  VOILA_BASE_URL="/user/${JUPYTERHUB_USER}/"
fi

# run based on the environment
voila /home/jovyan/japper_app/app.ipynb --Voila.base_url="$VOILA_BASE_URL"  --show_tracebacks=True --no-browser --Voila.ip=0.0.0.0 --Voila.root_dir=/home/jovyan/japper_app --port=8888 --preheat_kernel=True  --pool_size=5 --MappingKernelManager.cull_idle_timeout=300 --MappingKernelManager.cull_interval=60
