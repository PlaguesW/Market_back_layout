#Base model setup
FROM python:3.11.5

#Install requirements
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

#Copy app
COPY . /app/

#Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
