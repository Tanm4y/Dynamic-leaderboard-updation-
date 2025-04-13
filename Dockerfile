FROM python:3.12.7-slim

WORKDIR /app/

COPY pyproject.toml README.md ./
COPY TreeBoard /app/TreeBoard
RUN python -m pip install .

WORKDIR /app/TreeBoard
EXPOSE 8000
CMD python -m flask run --port 8000 --host 0.0.0.0