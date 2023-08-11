FROM python:3.9-alpine3.17

WORKDIR /usr/src/app

RUN apk add --no-cache make

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["make", "run"]
