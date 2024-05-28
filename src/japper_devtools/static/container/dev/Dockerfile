FROM jupyter/base-notebook

# setup conda environment
COPY ./environment.yml /home/jovyan/.
RUN mamba env update -n base --file /home/jovyan/environment.yml
ADD --chown=jovyan:users ./container/dev/start.sh /home/jovyan/.
RUN chmod +x /home/jovyan/start.sh

# depress the warning message
ENV PYDEVD_DISABLE_FILE_VALIDATION=1

# launch voila and jupyter lab
CMD /bin/bash start.sh