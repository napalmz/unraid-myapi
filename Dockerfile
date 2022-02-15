FROM python:3.7
LABEL maintainer "NapalmZ <admin@napalmz.eu>"

WORKDIR /opt/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost:5000/ || exit 1

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]