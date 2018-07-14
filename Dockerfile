FROM tiangolo/uwsgi-nginx-flask:python3.6

# Install keras
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install keras
RUN pip3 install tensorforce

# Copy our code to app
COPY ./ /app

# Train network
# RUN python3 app/training.py
