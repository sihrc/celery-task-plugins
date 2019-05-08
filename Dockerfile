FROM indicoio/alpine:3.9.3

LABEL author="Chris Lee"
LABEL email="sihrc.c.lee@gmail.com"

ARG EXTRAS="[test]"
ENV PATH=/celery_task_plugins/bin:${PATH}

COPY . /celery_task_plugins
WORKDIR /celery_task_plugins

RUN pip3 install --find-links=/root/.cache/pip/wheels -e .${EXTRAS} && \
    python3 setup.py develop --no-deps

CMD ["bash"]
