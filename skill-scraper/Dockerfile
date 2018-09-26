#  Docker image for the skill-scraper application.
#  The image copies the complete application
#  directory and starts a Sanic server. 


FROM python:3.6
ENV TZ=America/New_York

#  Setting up timezone to EST (New York).

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt /skill-scraper/requirements.txt


WORKDIR "/skill-scraper"
RUN pip install -r requirements.txt

COPY . /skill-scraper
CMD ["python", "run.py"]
