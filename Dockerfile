FROM python:3.6-stretch
RUN mkdir /code
WORKDIR /code
EXPOSE 80
ADD requirements.txt /code/
RUN pip install -qr requirements.txt
ADD . /code/
CMD [ "/code/launch.sh" ]
