FROM tiangolo/uvicorn-gunicorn:python3.10
WORKDIR /backend
RUN pip3 install pydantic fastapi sqlalchemy requests PyJWT passlib
COPY backend/ .
CMD ["uvicorn", "backend_api:app", "--host", "0.0.0.0", "--port", "8000"]