FROM jupyter/base-notebook:notebook-6.4.0

# setup conda environment
COPY ./environment.yml /home/jovyan/.
RUN mamba env update -n base --file /home/jovyan/environment.yml
ADD --chown=jovyan:users ./container/appmode/start.sh /home/jovyan/.
RUN chmod +x /home/jovyan/start.sh

# depress the warning message
ENV PYDEVD_DISABLE_FILE_VALIDATION=1

RUN pip install appmode && \
    jupyter nbextension     enable --py --sys-prefix appmode && \
    jupyter serverextension enable --py --sys-prefix appmode

#CMD ["jupyter-notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token=''"]
CMD /bin/bash start.sh

