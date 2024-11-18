# Relatório do TP6
## Data:19/10/2024
## Autor: João Dinis Dias Pereira A107192

## Resumo:

O TP6 consistiu na criação de uma aplicação que permite criar e guardar turmas.
A aplicação, semelhante a trabalhos anteriores, contem funções que permitem criar uma turma, listá-la e consultar elementos pertencentes à turma.
A principal diferença em relação a TPCs anteriores é o ato de guardar e carregar informação de um ficheiro. Como tal vou focar-me nesses dois aspetos:
* 1 - Guardar: para guardar informação num ficheiro a função primeiro abre um ficheiro (se esse ficheiro já existir o conteúdo anterior é apagado). Depois escreve a informação no ficheiro em *strings* dividindo a informação relevante entre separadores como (/ ou -).

* 2 - Carregar: para carregar informação de um ficheiro, a função abre o ficheiro com o nome introduzido e lê a informação existente. Depois, separa o texto no ficheiro com *split* dos separadores usados anteriormente para obter a informação da turma. No final,insere essa informação na estrutura de dados utilizada na aplicação (uma lista de tuplos em que cada tuplo representa um aluno).

Por fim, foi necessário criar um menu tal como trabalhos anteriores e uma turma de cinco alunos, cujo ficheiro também está na pasta TP6.