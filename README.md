# ML Model Deployment

## Objetivo:
Fazer o deploy de um modelo simples de regressão linear, hospedando o código em um container no ECR e vinculando em uma AWS Lambda Function com um agendamento definido.

<br>

## Roadmap

1- Criar Modelo

2- Desenvolver script de treinamento e push do modelo

3- Desenvolver script de inferência

<br>

## Infraestrutura

<br>

## Referências

<br>

## Utilização

<br>

### Deploy do modelo

1- Definição das variáveis de ambiente:

```shell
 $ export AWS_SECRET_ACCESS_KEY=<user-aws-secret-key>
 $ export AWS_ACCESS_KEY_ID=<user-aws-access-key-id>
 $ export ARTIFACT_BUCKET_NAME=<nome-do-bucket-de-artefatos>
 $ export INFERENCE_BUCKET_NAME=<nome-do-bucket-de-inferencia>
```


 2- Instalação de dependências
 ```shell
 $ make install
```

 3- Cria infraestrutura para inferência
 ```shell
 $ make inference-infra
```

 4- Execução do pipeline de treinamento do modelo
 ```shell
 $ make training-pipeline
```

<br>

### Execução dos Testes

1- Definição das variáveis de ambiente:

```shell
 $ export ARTIFACT_BUCKET_NAME=<nome-do-bucket-de-artefatos>
 $ export INFERENCE_BUCKET_NAME=<nome-do-bucket-de-inferencia>
```

 2- Instalação de dependências
 ```shell
 $ make install
```

 3- Execução dos testes
 ```shell
 $ make tests
```