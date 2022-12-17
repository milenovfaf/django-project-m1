FROM python:3.8-slim-buster

# Collecting django-ckeditor==6.3.2
# pip._vendor.urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out.
RUN mkdir ~/.pip && \
cd ~/.pip/  && \
echo "[global] \ntrusted-host =  pypi.douban.com \nindex-url = http://pypi.douban.com/simple" >  pip.conf


WORKDIR /app/src

COPY ./src/web_site/             /app/src
COPY ./requirements.txt     /app/src/requirements.txt


RUN pip3 install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE='web_site.settings.development'

RUN mkdir -p /app/data
ENV SITE_DIR='/app/data'
# collectstatic после runtime volume

EXPOSE 8001
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8001"]

