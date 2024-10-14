# Relatório do TP3
## Data:29/09/2024
## Autor: João Dinis Dias Pereira A107192

## Resumo:
O TP3 consistiu na elaboração de um jogo chamado "21 fósforos" cujas regras são: 

* No início do jogo, há 21 fósforos; 

* Cada jogador pode tirar 1 a 4 fósforos quando for a sua vez de jogar; 

* Os jogadores jogam alternadamente; 

* O último a tirar um fósforo perde. 

 

As especificações do programa eram que: 

 

* O jogo deve ter dois modos: num o utilizador começa e no outro o computador começa; 

* Quando o computador começa a jogar em segundo, deve ganhar sempre o jogo; 

* Quando o computador começa a jogar em primeiro lugar, se o utilizador cometer um erro de cálculo, o computador deverá passar para a posição de vencedor e ganhar o jogo. 


Primeiro comecei pelo modo no qual o computador joga em segundo e tem de ganhar sempre. Neste caso a estratégia que eu usei foi: utilizando um ciclo *while* retirar a uma variável *fosforos* o número dado pelo utilizador. Depois retirava à mesma variável 5-jogada do utilizador, o que seria a escolha do computador. A razão deste raciocínio é: se o segundo jogador (neste caso o computador) escolher um número que somado ao anterior dá 5, o total de fósforos desce por 5. Ao chegar à quinta ronda isto assegura que o primeiro jogador é forçado a tirar o último fósforo pois 21-5-5-5-5=1. 

 

No segundo modo utilizei um raciocínio parecido. Como o jogo está dependente em fazer combinações de 5 para chegar até 1, o segundo jogador ganha sempre se jogar perfeito pois é ele que acaba a combinação. Então se o segundo jogador fizer um erro de cálculo, como estava previsto nas especificações, é possível o primeiro jogador ganhar se ele completar as combinações de 5. 

Para conseguir isto, pus uma condição para o programa detetar sempre que a soma das jogadas do computador e utilizador fosse diferente de 5. Visto que é só necessário um erro de cálculo para assegurar a vitória do primeiro jogador eu inseri uma segunda variável *erro* na condição. A condição só seria verdadeira se *erro* tivesse valor 1, mas depois de encontrar um erro de cálculo o programa muda a variável para 0 garantindo que a condição não se repete. 

Após encontrar um erro de cálculo o programa verifica se a soma é maior ou menor do que 5. Caso seja maior o programa faz com que a escolha do computador seja 10-a soma, pois 10 é o dobro de 5. Se for menor a escolha passa a ser 5-a soma. Agora para o computador vencer só tem de fazer combinações de 5 com as jogadas do utilizador ou seja 5-a jogada. 

```
if n+comp!=5 and erro==1: 
    if n+comp<5: 
        comp=5-(n+comp) 
    else: 
        comp=10-(n+comp) 
    erro=0 
else: 
    comp=5-n 
```

A seguir, inseri nos dois modos condições de forma a avisar caso opções inválidas fossem escolhidas (como tentar tirar 5 fósforos) e para o jogo acabar quando a variável *fosforos* fosse igual a 0. No final criei um menu que dependendo da opção escolhida chama a função correspente ao modo.

 