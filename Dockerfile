FROM tiangolo/uwsgi-nginx-flask:flask

# Copy requirements to tmp
COPY requirements.txt /tmp/

# Upgrade pip and install required python packages
RUN pip3 install -U pip
RUN pip3 install -r /tmp/requirements.txt

# Copy over our app code
COPY ./app /app

# TODO: Train network
# RUN python3
