# SENSECOVID: COVID-19 Twitter Analyzer
Welcome to project sensecovid! This is an intelligent online system that can automatically aggregate and summarize valuable information from live streaming tweets around COVID-19 related topics.

**Note:** Please feel free to visit our website via www.sensecovid.info 

## System Architecture Overview

![System Architecture](./imgs/sys-architecture.png)

## Environment Preparation

1. #### **Twitter-side setup**

    -  Create a new app at [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard) 

    -  Save your **Consumer Keys** and **Authentication Tokens**

2. #### **Server-side setup**

    - **Create a conda virual enviroment**
        - `conda create -n twitter python=3.7`
    - **Install all required packages**
        - `conda activate twitter`
        - `pip install -r requirements.txt`
    - Set up credentials for [twarc](https://github.com/DocNow/twarc) ( **Consumer Keys, etc)**
        - `twarc config`

## Initiate the system

For this part, there are several different modules needs to be run simultaneously, you may want a terminal multiplexer like tmux to multiprocess these programs as well as monitor their status.

Before start the actual python scripts, please activate the required enviroment by:

`conda activate twitter`

1. **Start the Back-end system**
   - Go into [backend](./backend/) folder, this is the place we store all backend dependencies
     - `python senti_workflow.py`
     - `python Data/twitter_listener.py`
       - **Note:** For this part to run, please put your own twitter confidentials in the [twitter_listner.py](./backend/Data/twitter_listener.py)
     - `python Data/spark_engine.py`
   - Then go into [backend/Summarization](./backend/Summarization) folder
     - `python sum_updator.py`
2. **Start the Front-end system**
   - Go into [sensecovid](./sensecovid/) folder, this is the place we store all front-end dependencies
     - `python sensecovid.py`

