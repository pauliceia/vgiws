# Create a image based on the official image of python 3.5
FROM python:3.5

# Create a default folder to run the code
WORKDIR /usr/src/vgiws

# Copy the file with the dependencies to inside the workdir
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && apt-get install -y dialog apt-utils && \ 
    apt-get install -qqy software-properties-common --no-install-recommends && \
    apt-get install -y python-gdal python3-gdal gdal-bin

# Fix the timezone
ENV TZ=America/Sao_Paulo

# Expose the port
EXPOSE 8888

# Run this command when the container is created. The flag "-u" is to print the "print()"
CMD [ "python", "-u", "main.py"]

# Declare the default values to the arguments
#ENV debug=False
#ENV publish_layers_in_geoserver=True
#CMD [ "python", "-u", "main.py ${debug} ${publish_layers_in_geoserver}"]
