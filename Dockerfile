FROM python:3.9-alpine

RUN pip install --upgrade pip


RUN addgroup -g 65532 nonroot
RUN adduser -u 65532 -G nonroot -h /home/nonroot -D nonroot


WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

USER 65532:65532
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]