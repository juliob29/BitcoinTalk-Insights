#
#  Docker image for the skill-template application.
#  The image copies the complete application
#  directory and starts a Sanic server. 
#
FROM python:3.6
ENV TZ=America/New_York

#
#  Setting up timezone to EST (New York).
#
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt /skill-crypto/requirements.txt
COPY ./vendor /skill-crypto/vendor
WORKDIR "/skill-crypto"

RUN pip install pip --upgrade && pip install -r requirements.txt
RUN python -m nltk.downloader wordnet
RUN python -m spacy download en

COPY . /skill-crypto

ENV  MODELS_PATH=models

EXPOSE 8000

CMD ["bash", "run.sh"]
