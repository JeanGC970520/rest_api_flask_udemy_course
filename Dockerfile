FROM python:3.12.4
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /app
CMD [ "flask", "run", "--host", "0.0.0.0" ]