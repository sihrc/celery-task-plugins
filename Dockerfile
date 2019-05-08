FROM indicoio/alpine:3.9.3

LABEL author="Chris Lee"
LABEL email="sihrc.c.lee@gmail.com"

ARG EXTRAS="[test]"

COPY . /celery-task-plugins
WORKDIR /celery-task-plugins

RUN pip3 install --find-links=/root/.cache/pip/wheels .${EXTRAS} && \
    python3 setup.py develop --no-deps

CMD ["bash"]
