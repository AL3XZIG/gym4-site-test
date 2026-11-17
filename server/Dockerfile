FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN groupadd --system --gid 10001 gym4 \
    && useradd --system --uid 10001 --gid gym4 --home-dir /app --shell /usr/sbin/nologin gym4

WORKDIR /app
COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY server/ /app/
RUN mkdir -p /app/staticfiles /app/private_media \
    && chown -R gym4:gym4 /app

USER gym4
EXPOSE 8000
CMD ["sh", "/app/entrypoint.sh"]
