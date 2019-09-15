FROM python:3.7
ADD vrticl/utility /
CMD [ "python", "./utility.py" ]
