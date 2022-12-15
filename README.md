
# SurvAI Speech to Text Repository

This repo contains the SurvAI speech to text model along with the meta script that allows the appropriate JSON data to be exported to the web. The repo is designed to be activated using a docker container generated from the contained Dockerfile, which will download a video using a given MUX url, split audio from the video, and run the speech to text model on that audio file. It will then output the unique video id, the detected language of the video, the full transcript, and timestamped segments of the transcript. If the model detects a language other than english, the transcript will automatically be translated to english. For local use, there is an optional ‘--folder’ command line argument where you can specify a local folder of videos to run the model on as well as a ‘--save-output’ argument that will save the json data to your local directory. 


## Environment Setup for Local Use

### Requirements
- CUDA 11.3
- Pytorch 11.2.1
- Python 3.9
- Conda (up to date)
- GPU (optional, but highly recommended)

### Installation Instructions

1. ) In your terminal, cd’ed to the desired directory to store the repo, run:
- ```git clone https://github.com/Survai-hrf/speech-recognition.git```

2. ) With miniconda3 installed on your local machine, in your terminal run:
- ```conda create -n <MY ENV> python=3.9```
- ```conda activate <MY ENV>```

3. ) If using a gpu, run:
- ```pip install -r gpu_requirements.txt``` 

4. ) If not using a gpu, you can optionally run:
- ```pip install -r requirements.txt``` 

The gpu_requirements.txt will still work if running on cpu as the model will default to cpu usage if no gpu is detected, but the gpu packages will take up slightly more space on your hard drive, so it is recommended to use this method if you do not intend to use a gpu.


## API Description

The API endpoint accepts the following parameters:
1. ) Mux url (ex: https://stream.mux.com/piyBzpj801bLPqwUsAZj2oQNEeSJVZNkNPTf3zuuXSaE/high.mp4?download=test.mp4)

2. ) Unique video id

The api will then download the video, split the audio, process the audio, and send the json data back to the web as described in the introduction.

NOTE: to use the api endpoint, you must be connected to the appropriate AWS queue. To connect to the AWS queue, you must have the following information in a .env file:
- REGION_NAME=” ”
- AWS_ACCESS_KEY_ID=” ”
- AWS_SECRET_ACCESS_KEY=” “
- QUEUE_URL=” “

## Instructions for Local Inference

To process videos in the AWS queue, cd into the speech-recognition repo and run:
- ```python src/run_speech.py```

This will process each video in the queue using first in first out.

To run on a local folder of videos and save the json output data to your local directory, run:
- ```python src/run_speech.py - -folder <PATH/TO/FOLDER> - -save-output```

run_speech.py accepts the following arguments:

- "video_id" (required, automatically generated)
- "model" (required, automatically generated)
- "--folder" 
- "--save-output"

### --folder
Specifies the path to a local folder containing videos. The script will automatically filter out other file types, so it is okay to pass a folder containing other files like txt or csv.

### --save-output
Specifies to save the JSON output data to a folder named ‘output_files’. Each json will be named after the respective video file name.


## Docker

To build the docker image, once cd’ed into the ‘speech-recognition’ directory on your local machine, run:
- ```docker image build -t <MY IMAGE> .```

To run the docker image, run:
- ```docker run <MY IMAGE>``` 

In its current state, the command specified in the Dockerfile will search for a message/messages in survai’s speech-recognition AWS queue and process each. If there are no messages detected, the docker container will be stopped. 


## Notebooks
Inside the notebooks folder, there are two supplemental jupyter notebooks:

### set_threshold.ipynb
One of the limitations of the model is its ability to accurately detect the correct language of audio files where the audio is severely jumbled or low quality. If the model detects the wrong language, the resulting transcript will be wildly inaccurate. To combat this, it is necessary to break the script if the language confidence is below a certain threshold. To determine this threshold, this notebook uses a folder of videos tagged with their correct language. It will then use the speech to text model to predict the language in the video and compare the prediction to the correct language to determine if its prediction is correct. It will then calculate the average confidence score of correct and incorrect predictions, as well as the minimum correct confidence versus maximum incorrect confidence to provide a window to set the threshold. To add videos to the ground_truth.json, simply add a key, value pair to the dictionary in the following format: “<videos/VIDEO NAME>”: {“language”: “<LANGUAGE ABREV>”} (i.e. the same format as the others). NOTE: Any videos added to the ground truth json require the abbreviated language tag (use ‘languages.json’ for reference)

### test.ipynb
A testing ground for altering the model, adding features, or quickly transcribing a single video or audio file.