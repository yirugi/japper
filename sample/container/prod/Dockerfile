FROM jupyter/base-notebook

USER root

COPY environment.yml /tmp/.
RUN chmod 777 /tmp/environment.yml

USER jovyan
# setup conda environment
RUN mamba env update -n base --file /tmp/environment.yml

# copy app file
RUN mkdir /home/jovyan/japper_app
COPY --chown=jovyan:users app.ipynb /home/jovyan/japper_app/.
COPY --chown=jovyan:users app /home/jovyan/japper_app/app

RUN chmod 755 /home/jovyan

CMD voila /home/jovyan/japper_app/app.ipynb --Voila.base_url="/user/$JUPYTERHUB_USER/"  --show_tracebacks=True\
    --autoreload=True --no-browser --Voila.ip=0.0.0.0 --Voila.root_dir=/home/jovyan/japper_app --port=8888
