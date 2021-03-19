FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

RUN python -m ipykernel install --user

ADD ./jupyter/covid_graph_nrw.ipynb /home/jovyan/nb.ipynb

# ENV STATIC_URL /static
# ENV STATIC_PATH /var/www/app/static

COPY main.py /app/
COPY uwsgi.ini /app/
COPY app/__init__.py /app/app/
COPY app/views.py /app/app/
