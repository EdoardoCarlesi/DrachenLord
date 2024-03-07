FROM python:3.11

WORKDIR /app

RUN git clone https://github.com/EdoardoCarlesi/DrachenLord.git .

#RUN apt-get install portaudio-dev python-all-dev

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
