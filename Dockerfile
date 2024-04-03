FROM python:3.12-alpine as base
FROM base as builder
COPY requirements-dev.txt /requirements-dev.txt
RUN pip install --user -r /requirements-dev.txt

FROM base
COPY --from=builder /root/.local /root/.local
COPY main.py /app
COPY Helper /app/Helper
COPY custota-tool /app
WORKDIR /app
RUN ls -la

# update PATH environment variable
ENV PATH=/home/app/.local/bin:$PATH

EXPOSE 5000
CMD ["python", "-u", "main.py"]
