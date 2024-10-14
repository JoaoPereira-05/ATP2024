# Relatório do TP4
## Data:5/10/2024
## Autor: João Dinis Dias Pereira A107192

## Resumo:
O TP4 consistiu em fazer uma aplicação para manipular listas de inteiros. Esta aplicação contém opções como:
 * Criar ou ler uma lista;
 * Somar, subtrair ou fazer a média;
 * Identicar o número maior ou menor;
 * Verificar se está ordenada de forma crescente ou decrescente;
 * Procurar um elemento;
 *Sair.


Depois de criar estas opções também foi necessário criar um menu.

Para começar criei uma função para cada opção:

* 1 - Criar uma lista: Aqui fiz uma função que recebe um número inteiro e devolve uma lista, que por cada número em *range(N)*, insere um número aleatório entre 0 e 100;
* 2 - Ler uma lista: Nesta opção a função recebe um número inteiro e usa um ciclo *while* para pedir N números inteiros, e adiciona cada número inteiro à lista;
* 3 - Somar: Uma função que recebe uma lista e usa um ciclo *for* para somar os elementos da lista;
* 4 - Média: A função tem a condição de que se a lista tiver 0 elementos o resultado é zero(de forma a evitar a divisão por 0). No caso de não ter 0 elementos, a função soma os elementos da mesma maneira que a função de Somar e depois divide pelo comprimento da lista(*len(lista)*);
* 5 e 6 - O maior e o menor da lista: Uma função que usa uma variável igual ao primeiro elemento da lista(*lista[0]*), usando um ciclo *for*, substitui essa variável da lista caso seja maior ou menor dependendo da opção. O resultado no final irá ser o número maior/menor.
* 7 e 8 - Está ordenada de forma crescente/decrescente: Para esta opção criei uma função que usa duas variáveis *res* e *i* (*res* tem valor inicial não e *i* tem 1). A seguir inseri um ciclo *while* que repete enquanto uma variável *i* é menor do que a *len(lista)*, sendo que *i* aumenta em 1 cada vez que o ciclo itera. No final, pus uma condição que compara o índice *i** da Lista com o *i-1*, por esta razão *i* tem o valor inicial 1 (se i começasse em zero a função compararia o primeiro elemento com o último). Se encontrar algo de errado dependendo da opção(crescente ou decrescente), *res* fica igual "Não".

```
#Exemplo da função de ordenação crescente
def estaOrdenadaC(lista):
    i=1
    res="Sim"
    while i<len(lista):
        if lista[i]< lista[i-1]:
          res="Não"
        i=i+1
    return res
```

* 9 - Procurar um elemento: Em último uma função que receba uma lista e um elemento. Usei duas variáveis e um ciclo *while* de forma a poder parar o ciclo a meio. O ciclo itera sempre que *i* menor que *len(lista)* e *res ==-1*. Depois criei uma condição que compara o índice *i* com o elemento. Caso sejam iguais, *res* fica igual a *i* dando assim o índice do elemento e caso o elemento não exista *res* fica igual a -1.

``` 
def unicos2(lista,elem):
    res=-1
    i=0
    while i < len(lista) and res==-1:
        if lista[i]== elem:
            res=i
        i=i+1
    return res
```



No final criei um ciclo *while* que continua enquanto a opção não for 0, que faz print do menu e que chama a função correspondente a cada opção. 

