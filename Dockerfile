FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
RUN apt-get install graphviz -y
RUN apt-get install graphviz-dev -y
RUN pip3 install pygraphviz

RUN apt-get install -y libgdal-dev g++ --no-install-recommends && \
    apt-get install gettext -y && \
    apt-get clean -y

RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal


# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["api.py" ]