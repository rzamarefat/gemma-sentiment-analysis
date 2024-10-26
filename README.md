# Gemma2 Sentiment Analysis
An implementation of fine-tuning Gemma2 model on sentiment analysis and a full-stack web app for serving it


## How to run (Without Docker)

1. back
- Create a Python3 virtual env
- Activate the environment creatred in the previous step
- cd to back folder
- install the requirements in requirements.txt file
- run the following command
```
uvicorn main:app --port 8086  --reload
```

2. front
- cd into front folder
- run the following command to install the dependencies (you need Node installed on your machine)
```
npm install .
```
- run the following command to start the front-end
```
npm start
```

## How to run (With Docker)
1. back
- cd into back folder
- run the following command to build the docker image
```
docker build -t gemma-sent-analysis-app .
```
- run the following command to run the docker container
```
docker run -p 5000:5000 gemma-sent-analysis-app
```
2. front
- cd into front folder
- run the following command to build the docker image
```
docker build -t gemma-sent-analysis-app-react .
```
- run the following command to run the docker container
```
docker run -p 8080:80 gemma-sent-analysis-app-react
```

