FROM python:3.12-alpine as base
FROM base as builder
COPY requirements-dev.txt /requirements-dev.txt
RUN pip install --user -r /requirements-dev.txt

FROM base
COPY --from=builder /root/.local /root/.local
COPY src /app
WORKDIR /app

# update PATH environment variable
ENV PATH=/home/app/.local/bin:$PATH

CMD ["/bin/sh"]
