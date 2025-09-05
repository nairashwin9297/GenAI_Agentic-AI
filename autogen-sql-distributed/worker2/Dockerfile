FROM python:3.11-slim
RUN pip install --upgrade pip
RUN pip install --upgrade pip
RUN pip install autogen-core autogen-agentchat autogen-ext grpcio grpcio-tools openai tiktoken numpy
COPY shared /app/shared
COPY worker2/run_worker2.py /app/
WORKDIR /app
CMD ["python", "-u", "run_worker2.py"]