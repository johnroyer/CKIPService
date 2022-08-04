# CKIP Service
Docker compose for [ckiplab/ckiptagger](https://github.com/ckiplab/ckiptagger)

This version is for aarch64 (Pi 4 model B). Base image is build by [armswdev/tensorflow-arm-neoverse](https://hub.docker.com/r/armswdev/tensorflow-arm-neoverse).

## Preparation
- [Download model files](https://github.com/ckiplab/ckiptagger#1-download-model-files) and put into `data` folder

## Start service
1. Start the service using `docker-compose`
    ```
    docker-compose up -d
    ```
    If you want to rebuild the image, add `--build` flag when startup
    ```
    docker-compose up --build -d
    ```
2. Service is now on port `5005`

## Stop service
1. Stop the service using `docker-compose`
    ```
    docker-compose down
    ```

## Endpoint
- Main
    - method: `POST`
    - route: `/`
    - parameter
        - `sentence_list`: sentence list for CKIP tagging, split multiple sentences by linebreak(`\n`)

## Test CKIP Tagger
1. Send request using curl
    ``` bash
    curl -X POST localhost:5005 -F $'sentence_list=土地公有政策?？還是土地婆有政策。.\n最多容納59,000個人,或5.9萬人,再多就不行了.這是環評的結論.'
    ```
2. Get the response like the following one
    ```
    土地公(Nb)　有(V_2)　政策(Na)　?(QUESTIONCATEGORY)　？(QUESTIONCATEGORY)　還是(Caa)　土地(Na)　婆(Na)　有(V_2)　政策(Na)　。(PERIODCATEGORY)　.(PERIODCATEGORY)　
    (0, 3, 'PERSON', '土地公')

    最多(VH)　容納(VJ)　59,000(Neu)　個(Nf)　人(Na)　,(COMMACATEGORY)　或(Caa)　5.9萬(Neu)　人(Na)　,(COMMACATEGORY)　再(D)　多(D)　就(D)　不行(VH)　了(T)　.(PERIODCATEGORY)　這(Nep)　是(SHI)　環評(Na)　的(DE)　結論(Na)　.(PERIODCATEGORY)　
    (4, 10, 'CARDINAL', '59,000')
    (14, 18, 'CARDINAL', '5.9萬')
    ```

## Alternative
If you want to run this service without Docker, you can follow this steps after `data` folder is ready.  
However, **we highly recommend using Docker Compose**.
1. Install required packages
    ```bash
    pip3 install -r requirements.txt
    ```
2. Run
    ```bash
    python3 ckip_service.py
    ```
