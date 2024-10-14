# Relatório do TP5
## Data:13/10/2024
## Autor: João Dinis Dias Pereira A107192

## Resumo:
O TP5 consistiu em criar uma aplicação para gerir um cinema de um centro comercial. Como tal esta aplicação tem opções como:
* Adicionar ou verificar salas de cinema;
* Verificar lugares disponíveis, um lugar específico e comprar bilhetes dependendo do filme;
* Listar o cinema e fazer reset do sistema.

É também necessário criar um menu de interface para a aplicação.

Neste TP primeiro criei um menu com um ciclo que itera sempre que a opção é diferente de zero; criei uma lista vazia chamada *cinema* e a variável *opcao*, que vai guardar a informação relativa às salas de um cinema e a opção escolhida respetivamente. A seguir comecei a fazer as funções para cada opção. As funções foram feitas usandos ciclos *for* e desempacotando tuplos:

* 1 - Reset: Simplesmente torna *cinema* numa lista vazia;
* 2 - Inserir Sala: Nesta opção existem duas funções: uma que verifica se a sala já existe em *cinema* e outra que dependendo da resposta da primeira adiciona a sala à lista *cinema*;
* 3 - Listar o cinema: Simplesmente mostra a listagem das salas e dos filmes correspondentes em *cinema* ;
* 4 - Lugar específico disponível: Uma função que usa um ciclo *for* para descobrir a sala em que está o filme e depois usa uma condição para ver se o lugar já foi vendido e depois responde *True* ou *False*.
```
def disponivel(cinema, nfilme, lugar):
    cond=False
    for sala in cinema:
        nlugares, Vendidos, filme= sala
        if filme == nfilme:
            if lugar not in Vendidos:
                cond=True
    return cond
```
* 5 - Comprar bilhete: Esta função chama a função anterior para ver se o lugar está diponível. Se estiver disponível adiciona o lugar à lista de lugares vendidos da sala.
* 6 - Ver lugares disponíveis: Esta função faz print de cada sala, o seu respetivo filme e o número de lugares disponíveis (nlugares- len(vendidos)).

Também acrescentei 2 funções que não estavam no exercício original:

* 7 - Remover sala: Esta função percorre a lista *cinema* e remove a sala com o nome introduzido na função.
* 8 - Devolver bilhete: Esta função recebe o nome da sala e um lugar e remove o lugar da lista de vendidos.

Finalmente, completei o menu chamando as funções específicas a cada opção, *prints* necessários e o que fazer no caso de o utilizador inserir opções inválidas.


