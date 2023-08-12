FROM python:3.10-slim

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content to the working directory
COPY src/ .

# Expose the API Port
EXPOSE 8080

# Run the server
CMD ["python", "app.py"]