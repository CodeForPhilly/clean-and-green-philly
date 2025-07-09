FROM python:3.11.4 AS tippecanoe
RUN apt-get update && apt-get -y install \
    make \
    gcc \
    g++ \
    libsqlite3-dev \
    zlib1g-dev
# TODO: Pin Tippecanoe to a specific version
RUN curl -L https://github.com/felt/tippecanoe/tarball/master -o tippecanoe.tar.gz \
    && mkdir tippecanoe && tar -xzf tippecanoe.tar.gz -C tippecanoe --strip-components=1 \
    && tar -xzf tippecanoe.tar.gz \
    && cd tippecanoe \
    && make \
    && make install

FROM python:3.11.4 AS dependencies
RUN curl -LsSf https://astral.sh/uv/0.7.12/install.sh | sh
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 PATH="/root/.local/bin/:$PATH"
WORKDIR /app
COPY uv.lock pyproject.toml ./
#TODO: in the future, remove development dependencies from final container
RUN uv sync --locked


FROM python:3.11.4

# Install system dependencies for GDAL and Tippecanoe
# TODO: Figure out which Tippecanoe dependencies we can remove since we've moved this to a
# separate stage
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    gcc \
    git \
    build-essential \
    libsqlite3-dev \
    zlib1g-dev \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

COPY --from=tippecanoe /usr/local/bin/tippecanoe /usr/local/bin/tippecanoe
COPY --from=tippecanoe /usr/local/bin/tile-join /usr/local/bin/tile-join
COPY --from=dependencies /app /app

ENV GDAL_VERSION=3.6.2 \
    GDAL_CONFIG=/usr/bin/gdal-config \
    # place .venv binaries copied from dependencies stage to front of PATH.
    # This includes python, pip, and individual package binaries
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY src ./src


CMD ["python", "-m", "src.main"]
