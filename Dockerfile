FROM armswdev/tensorflow-arm-neoverse:r23.07-tf-2.12.0-onednn-acl_threadpool

WORKDIR /usr/local/src/CKIPTagger

ADD requirements.txt .
RUN pip3 --no-cache-dir install -r requirements.txt

COPY ckip_service.py ./

EXPOSE 5005

CMD ["python3", "./ckip_service.py"]
