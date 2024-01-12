# Raízen Code Challenge - Wrapper de Previsão do Tempo

Esta aplicação fornece previsões do tempo para os próximos 5 dias para uma cidade especificada. Ela utiliza a API do OpenWeatherMap para obter dados meteorológicos e armazena essas informações em um banco de dados MongoDB para consultas rápidas e eficientes.

## Propósito

Esta API foi construída para o Code Challenge da Raízen (Qintess).

## Como Funciona

A aplicação consulta primeiro o banco de dados para verificar se a previsão do tempo recente para uma cidade específica já está armazenada.
Se os dados não estiverem disponíveis ou estiverem desatualizados (mais de 24 horas), a aplicação buscará as informações atualizadas da API do OpenWeatherMap.
A previsão do tempo é então atualizada no banco de dados e retornada ao usuário.

## Pré-requisitos

- Docker
- Docker Compose

## Configurar Variáveis de Ambiente

Defina as variáveis necessárias, como a chave da API do OpenWeatherMap, no arquivo .env.

## OpenWeatherMap API

Você pode utilizar a seguinte chave de API do OpenWeatherMap (expira em 30/01/2024)

    366050077c283577cb6bf100d0aa63ff

## Executar com Docker Compose

Use o comando docker-compose up --build para construir e iniciar os containers da aplicação e do MongoDB.

## Acessar a Aplicação

A aplicação estará disponível em http://localhost:8000/forecast/{city}, onde {city} é o nome da cidade desejada.

## Tecnologias Utilizadas

- FastAPI
- MongoDB
- Docker e Docker Compose
- OpenWeatherMap API

## Executar os testes

Para executar os testes basta instalar os pacotes necessários e executar o comando

    python -m tests.test_main test_wheater_service
