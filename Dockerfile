FROM python:3.9.2

COPY . .
RUN pip install -r requirements.txt
CMD python main.py
