FROM pytorch/pytorch:1.8.1-cuda10.2-cudnn7-runtime

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN python setup.py develop

CMD python parlai/chat_service/services/browser_chat/client.py
