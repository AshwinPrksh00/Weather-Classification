FROM python:3.7.12-buster

WORKDIR /Weather-Classification

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]