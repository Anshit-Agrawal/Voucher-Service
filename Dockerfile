FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install  --assume-yes python3-pip
RUN mkdir -p /voucher
COPY ./voucherServer.py /voucher/
COPY ./requirements.txt /voucher/
RUN /bin/bash -c "cd /voucher && pip3 install -r requirements.txt"
CMD ["/bin/bash" ,"-c", "cd /voucher && python3 voucherServer.py"]

