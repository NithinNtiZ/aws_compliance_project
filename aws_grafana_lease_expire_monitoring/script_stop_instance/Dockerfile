FROM python:3.12.2-alpine

WORKDIR /usr/src/app

ENV ACCESS_KEY=""
ENV SECRET_KEY=""
ENV DB_HOST=""
ENV DB_NAME=""
ENV DB_TABLE_NAME=""
ENV PYTHONDONTWRITEBYTECODE=1

COPY prod_stop_expired_instance.py  connection.py run.sh ./

# Set permissions and ownership
RUN adduser --disabled-password labadmin && \
    chown labadmin:labadmin prod_stop_expired_instance.py connection.py run.sh  && \
    chmod 700 all_instances.py connection.py run.sh

USER labadmin

CMD [ "./run.sh" ]