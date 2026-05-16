FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -m appuser
RUN python -c "import pathlib, streamlit; p = pathlib.Path(streamlit.__file__).parent / 'static' / 'index.html'; p.write_text(p.read_text().replace('<title>Streamlit</title>', '<title>Node Registry nodes</title>'))"
COPY app.py .
USER appuser
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
