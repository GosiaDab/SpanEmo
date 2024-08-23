FROM python:3.7.13-slim-bullseye

RUN apt-get update -y && apt-get install -y libpq-dev gcc apt-transport-https ca-certificates curl gnupg lsb-release

COPY requirements.txt .

RUN pip3 install torch==1.2.0+cpu torchvision==0.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt

COPY ./scripts /home
COPY ./models /home
COPY ./data /home
COPY ./configs /home

WORKDIR /home

ENTRYPOINT [ "tail" , "-f" , "/dev/null" ]