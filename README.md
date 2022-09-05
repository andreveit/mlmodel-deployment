# ML Model Deployment

## Objetivo:
Fazer o deploy de um modelo simples de regressão linear, hospedando o código em um container no ECR e vinculando em uma AWS Lambda Function com um agendamento definido.

<br>

## Infraestrutura

A infraestrutura foi organizada em 3 pilares, a ideia foi manter estes 3 o mais desacoplados possível.
### Repositório de modelos -> Bucket de artefatos

>A criação do bucket de artefatos, treinamento e push do modelo é feita de forma local

### Armazenamento dos dados -> Bucket de inferência

>A criação do bucket de inferência e push dos dados é feita de forma local


### Realização das predições -> Funcão Lambda

>A criação da função lambda para realização das predições é feita utilizando Serverless Framework 


<br>

## Roadmap

### 1- Modelagem
- Notebook de desenvolvimento do modelo


### 2- Pipeline de Treinamento
- Script de treinamento do modelo
- Classe para gerenciamento da infraentrutura (S3)
- Script de treinamento e push do modelo ao bucket de artefatos
- Criação de testes unitários


### 3- Infraestrutura de Inferência
- Script para criação de bucket de inferencia e push dos dados a serem consumidos pelo modelo


### 4- Script de Escoragem (Função Lambda)
- Construção de classes para seleção e obtenção do modelo do bucket de artefatos conforme a estratégia definida
- Script para escoragem dos dados de input e armazenamento das predições e metadados no bucket de inferência.


### 5- Testes de Integração
- Construção de infraestrutura local através de localstack e docker-compose 
- Criação de script python para validação da resposta da função lambda
- Desenvolvimento de script bash para orchestrar scripts python, criando a infraestrutura e testando a função lambda


### 6- Serverless Deploy
- Construção de script para push da imagem 
- Desenvolvimento do arquivo de configuração de deploy


### 7- CI/CD
- Arquivo ci.yml para realização dos testes para push/merge na branch develop
- Arquivo cd.yml para realização do deploy para push/merge na branch main

<br>


## Referências

- [DataTalksClub -  MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp)
- [Serverless Framework Documentation](https://www.serverless.com/framework/docs/providers/aws/guide/serverless.yml)
- [Serverless Framework Examples](https://github.com/serverless/examples)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Serverless GitHub Actions GitHub Repository](https://github.com/serverless/github-action)
- [AWS Wrangler Documentation](https://aws-sdk-pandas.readthedocs.io/en/stable/tutorials/004%20-%20Parquet%20Datasets.html)


<br>

## Utilização

### Pré-requisitos

- Docker
- Serverless Framework


<br>

### Deploy do modelo

**1- Definição das variáveis de ambiente e configurações**

 Secrets
 ```shell
export AWS_SECRET_ACCESS_KEY=<user-aws-secret-key>
export AWS_ACCESS_KEY_ID=<user-aws-access-key-id>
 ```

<br>

AWS Account ID

```shell
export ACCOUNT_ID=<aws-account-id>
```
ou 
```shell
export ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
 ```

<br>

Bucket names
 ```shell
export ARTIFACT_BUCKET_NAME=<nome-do-bucket-de-artefatos>
export INFERENCE_BUCKET_NAME=<nome-do-bucket-de-inferencia>
```

<br>

 **2- Instalação de dependências**
 ```shell
 make install
```

 **3- Criação da infraestrutura para inferência**
 ```shell
make inference-infra
```

 **4- Execução do pipeline de treinamento do modelo**
 ```shell
make training-pipeline
```

 **5- Deploy da função lambda de escoragem**
 ```shell
make deploy
```

<br>

### Execução dos Testes

**1- Definição das variáveis de ambiente**

```shell
 $ export ARTIFACT_BUCKET_NAME=<nome-do-bucket-de-artefatos>
 $ export INFERENCE_BUCKET_NAME=<nome-do-bucket-de-inferencia>
```

 **2- Instalação de dependências**
 ```shell
 $ make install
```

 **3- Execução dos testes**
 ```shell
 $ make tests
```