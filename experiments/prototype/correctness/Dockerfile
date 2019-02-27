FROM python:latest
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp
RUN pip install numpy
CMD [ "python","./test_correctness.py" ]
