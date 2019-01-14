FROM gcc:4.9
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp
RUN gcc -o myapp -std=gnu99 ./getpid.c
ENTRYPOINT ["./myapp"]
