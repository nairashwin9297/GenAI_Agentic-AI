FROM python:3.11-slim
RUN pip install autogen-core autogen-ext grpcio grpcio-tools
COPY shared /app/shared
COPY worker1/run_worker1.py /app/
WORKDIR /app
CMD ["python", "-u", "run_worker1.py"]