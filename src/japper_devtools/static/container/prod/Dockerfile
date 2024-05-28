FROM jupyter/base-notebook

# setup conda environment
COPY ./environment.yml /home/jovyan/.
RUN mamba env update -n base --file /home/jovyan/environment.yml
ADD --chown=jovyan:users ./container/prod/start.sh /home/jovyan/.
RUN chmod +x /home/jovyan/start.sh

# copy app file
RUN mkdir /home/jovyan/japper_app
COPY --chown=jovyan:users app.ipynb /home/jovyan/japper_app/.
COPY --chown=jovyan:users app /home/jovyan/japper_app/app

RUN chmod 755 /home/jovyan

CMD /bin/bash start.sh