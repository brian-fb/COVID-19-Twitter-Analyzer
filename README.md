# COVID-19-Twitter-Analyzer
## System Architecture Overview

![System Architecture](./imgs/sys-architecture.png)

## Environment Preparation

1. **Twitter-side setup**

    -  Create a new app at [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard) 

    - Save your **Consumer Keys** and **Authentication Tokens**

2. **De-hydrated COVID-19 Twitter set**

    -  Download the latest filtered data from [IEEEDataPort](https://ieee-dataport.org/open-access/coronavirus-covid-19-tweets-dataset)

3. **Twitter data hydrator set-up**

    -  Install [twarc](https://github.com/DocNow/twarc): 

      ```
      pip install twarc
      ```

    -  Set up credentials ( **Consumer Keys, etc)**

      ```
      twarc config
      ```

## Preparation
