FROM python:3.4
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
EXPOSE 8000
ADD . /code/
CMD [ "/code/launch.sh" ]