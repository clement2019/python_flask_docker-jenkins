FROM python:alpine
ADD . /app
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
COPY . .
EXPOSE 5002
ENTRYPOINT ["python","app.py"]