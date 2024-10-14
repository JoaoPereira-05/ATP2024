# Relatório do TP2
## Data:22/09/2024
## Autor: João Dinis Dias Pereira A107192

## Resumo:
O TP2 consistiu na realização de um jogo. Este jogo tinha como objetivo advinhar um número entre 0 e 100 e ter 2 modos: o computador pensa num número e o jogador tenta adivinhar ou vice-versa:

* Quem tenta adivinhar responde com uma das afirmações: "Acertou", "O número que pensei é Maior" ou "O número que pensei é Menor";
* Quando o jogo acaba, o programa imprime o número de tentativas.

Ao fazer este trabalho, primeiro comecei pelo modo no qual o computador advinha o número do utilizador (porque era o mais difícil). Para tal baseei-me no raciocínio de que a melhor advinha será sempre o número equidistante entre o menor e o maior número possível(ou seja a média dos dois). Assim, o programa que criei tem 2 variáveis para guardar estes limites inferior e superior. 

Na primeira ronda estes limites são 0 e 100 respetivamente, o que significa que a primeira resposta do computador é sempre 50. Depois dependendo da resposta do utilizador estes limites variam: se o utilizador responder que o número é maior então a adivinha do computador passa a ser o novo limite inferior e se o utilizador responder menor, a adivinha passa ser o limite superior. Assim, ao usar a média entre os limites e ajustando-os baseados na respostas do utilizador, é possível encontar o número certo no menor número de tentivas.

```
if resposta=="O número que pensei é Maior":
    limit_inf = guess
    guess = (limit_sup+guess)//2
if resposta=="O número que pensei é Menor":
    limit_sup = guess
    guess= (limit_inf+guess)//2
```


O segundo modo foi mais fácil de executar. Neste caso simplesmente fiz o computador gerar um número aleatório e depois compará-lo com os números dados pelo utilizador. Após comparar, o programa responde se o número aleatório é maior ou menor até o utilizador acertar.

