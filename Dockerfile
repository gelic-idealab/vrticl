FROM python:3.7
ADD utility/utility.py /
CMD [ "python", "./utility.py" ]
