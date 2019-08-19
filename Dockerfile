FROM python:3.7
ADD utility.py /
CMD [ "python", "./utility.py" ]
