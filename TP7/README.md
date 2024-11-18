# Relatório do TP7
## Data:26/10/2024
## Autor: João Dinis Dias Pereira A107192

## Resumo:
O TP7 consistiu na criação de uma aplicação que permite criar e utilizar tabelas de dados meteorológicos.
Para tal efeito, funções de quatro tipos foram criadas:

* 1 - Uma função que permite criar uma tabela meteorológica com base nos dados inseridos:
    
    Esta função recebe *inputs* do utilizador e insere-os numa lista de tuplos (cada tuplo representa os dados de um dia).

* 2 - Uma função para guardar a tabela dentro de um ficheiro e outra para carregar de um ficheiro:
    
    A função de guadar usa um ciclo *for* para percorrer os dias da tabela e insere os dados numa string que depois é escrita dentro de um ficheiro.
    Já a de carregar faz o inverso: usa um ciclo *for* para percorrer as linhas do ficheiro e depois parte essas linhas(*split*) para obter as informações relevantes. No final essas informações são postas numa lista de tuplos semelhante à função de criar.

* 3 - Funções que calculam certas variáveis a partir de dados que se encontram nas tabelas:
    
    Usando ciclos *for* e desempacotando os tuplos correspondentes a cada dia, estas funções calculam variáveis como a temperatura média ou a amplitude térmica ou comparam valores entre dias como por exemplo o dia com maior precipitação.

* 4 - Funções que desenham gráficos dos dados das tabelas:
    
    Esta função acede às variáveis dentro da tabela meteorológica da mesma maneira que as funções de cima e faz gráficos com as variáveis usando o *matplotlib*.


Depois de criar as funções, criei um menu da mesma forma que trabalhos anteriores.