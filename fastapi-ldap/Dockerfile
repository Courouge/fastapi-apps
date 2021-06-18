FROM debian:buster-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes libsasl2-dev python-ldap libldap2-dev libssl-dev python3-venv && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM gcr.io/distroless/python3-debian10
COPY --from=build-venv /venv /venv
COPY --from=build-venv /usr/lib/x86_64-linux-gnu/ /usr/lib/x86_64-linux-gnu/
ENV LD_LIBRARY_PATH="/usr/lib"
COPY app /app
WORKDIR /app
EXPOSE 80
ENTRYPOINT ["/venv/bin/python3", "main.py"]