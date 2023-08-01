FROM python:3.11

WORKDIR /app

COPY . .

# use unbuffered output to see print output correctly in docker logs
# https://stackoverflow.com/a/29745541
CMD [ "python3.11", "-u", "main.py" ]
