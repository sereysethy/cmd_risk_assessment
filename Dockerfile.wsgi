FROM python:3.11-slim

RUN groupadd -g 1000 user && useradd --uid 1000 --gid 1000 --home /code user
USER user
WORKDIR /code

COPY --chown=user:user ./requirements.txt /code/requirements.txt

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY --chown=user:user ./app /code

ENTRYPOINT [ "/code/venv/bin/python3" ]

CMD ["/code/venv/bin/gunicorn", "main:app", "--workers 4", "--worker-class", \
    "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]