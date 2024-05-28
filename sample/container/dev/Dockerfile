FROM jupyter/base-notebook

USER root

COPY ./environment.yml /tmp/.
RUN chmod 777 /tmp/environment.yml

USER jovyan
# setup conda environment
RUN mamba env update -n base --file /tmp/environment.yml
ADD --chown=jovyan:users ./container/dev/start.sh /home/jovyan/.

# depress the warning message
ENV PYDEVD_DISABLE_FILE_VALIDATION=1

# launch voila and jupyter lab
CMD /bin/bash start.sh