FROM python:3.12.2-alpine

WORKDIR /usr/src/app

ENV ACCESS_KEY=""
ENV SECRET_KEY=""
ENV PYTHONDONTWRITEBYTECODE=1


COPY requirements.txt all_instances.py connection.py run.sh ./

RUN pip install --no-cache-dir -r requirements.txt

# Set permissions and ownership
RUN adduser --disabled-password labadmin && \
    chown labadmin:labadmin all_instances.py connection.py run.sh requirements.txt && \
    chmod 700 all_instances.py connection.py run.sh

USER labadmin

CMD [ "./run.sh" ]