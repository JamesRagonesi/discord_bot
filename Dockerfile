FROM python:3.8-alpine as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
ENV TZ="America/New_York"

# Create and switch to a new user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && apk add --no-cache tzdata
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY . .

# Run the application
CMD ["python", "-u", "bot.py"]
