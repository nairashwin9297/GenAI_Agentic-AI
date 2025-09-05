FROM python:3.11-slim
RUN pip install --upgrade pip
RUN pip install autogen-core autogen-ext grpcio grpcio-tools
COPY host/run_host.py /app/
WORKDIR /app
CMD ["python", "-u", "run_host.py"]