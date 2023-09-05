FROM lscr.io/linuxserver/blender:latest
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less python3 pip
RUN pip install requests 
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install numpy==1.23.1
RUN pip install opencv-python
RUN alias blender='/bin/Blender'
RUN pip install fastapi uvicorn 
RUN pip install replicate 
EXPOSE 8000

# 本番時、"--reload"は外す
CMD ["uvicorn", "api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]