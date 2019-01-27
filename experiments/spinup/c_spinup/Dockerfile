FROM gcc:7.3
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp
RUN gcc -o c_spinup -std=gnu99 ./c_spinup.c
CMD ["./c_spinup"]
