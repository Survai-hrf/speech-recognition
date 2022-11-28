FROM nvidia/cuda:11.3.1-devel-ubuntu20.04

ENV PYTHON_VERSION=3.9
ENV POETRY_VERSION=1.2.0
ENV POETRY_VENV=/app/.venv

CMD ['python', 'src/run_speech.py']