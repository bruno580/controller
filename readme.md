## Overview
This is a sample API in Python/Flask that runs on any given linux server and helps perform basic operations such as listing free storage space, free memory, etc.

## Getting started
On the linux machine you want to try this on, make sure you have Python 3.7 installed and install flask: `pip install flask`

Copy the app.py file to the location you want to run it from and run the command below:
```
flask run --host=0.0.0.0
```

## Usage
With the server running, you can use curl from any machine in your network to make requests. Examples below (please note the ip 10.0.0.73 is an example, replace with your linux machine's ip address):

--------
### Getting metadata:
```
curl --location --request GET 'http://10.0.0.73:5000/metadata'
```
Output:
```
[
    {
        "hostname": "ol7-base.dev.siselo.com",
        "kernel": "5.4.17-2102.201.3.el7uek.x86_64",
        "os-release": "Oracle Linux Server 7.9"
    }
]
```
--------
### Executing commands:
```
curl --location --request POST 'http://10.0.0.73:5000/command?command=memory_usage'
```
Output:
```
              total        used        free      shared  buff/cache   available
Mem:           3647        1114         158          74        2374        2224
Swap:          1535          37        1498
```
Note: 

You can replace the url argument `command` as desired, for example, if instead of getting memory usage I wanted to get disk usage, the url would be `command=disk_usage`. The commands are stored in the dictionary `command_whitelist`, just add more options and restart flask to test it out.

## Running from container
This is useful just for some local testing, to create a docker image, go to the same directory you have placed the file `app.py` and run the commands below.

- Create the Dockerfile:
```
cat << EOF > Dockerfile
FROM python:3.7-alpine

COPY . /app
WORKDIR /app

RUN pip install flask

CMD ["flask", "run", "--host=0.0.0.0"]
EOF
```
- Still in the same directory, run docker build:
```
docker build -t control-container .
```
- Once it finishes you can run the container:
```
docker run control-container
```
If everything is in order you should see something like:
```
[controller@ol7-base controller]$ docker run control-container
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.17.0.2:5000/ (Press CTRL+C to quit)
```