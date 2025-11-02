# arq2025.3.ufabc
PROJETO Arquitetura de Computadores

📖 Sobre o Projeto
Este projeto é um decifrador de cifras clássicas em Python, desenvolvido como parte de um trabalho prático sobre criptografia e representação numérica.

O objetivo principal é decifrar a mensagem contida no arquivo encoded.txt, que é um texto em inglês criptografado e, em seguida, convertido para binário (ASCII 7 bits).

O programa implementa dois ataques de criptoanálise:

Ataque de Força Bruta na Cifra de César.

Ataque de Otimização (Hill Climbing) na Cifra de Substituição Simples.

O núcleo do projeto é o uso de um modelo estatístico de Quad-grams (quadgrams.txt) para avaliar a "qualidade" (ou fitness) de um texto decifrado, permitindo que o programa "saiba" quando está se aproximando da solução correta.

🚀 Como Funciona
O script principal (cesardesc.py) oferece um menu interativo para escolher o método de ataque após carregar o arquivo codificado.

1. Ataque à Cifra de César (Opção 1)
Este é um ataque de força bruta simples.

Método: O programa testa todas as 25 chaves de deslocamento possíveis (de 1 a 25).

Avaliação: Para cada tentativa, o texto decifrado é pontuado usando o ngram_score.py.

Resultado: O programa exibe o texto com a maior pontuação. (Neste caso, o resultado é ilegível, provando que a cifra não é César).

2. Ataque à Cifra de Substituição (Opção 2)
Como o número de chaves de substituição (26!) é astronômico, a força bruta é impossível. Este ataque usa um algoritmo de otimização heurística chamado Hill Climbing (Subida de Encosta).

Método:

O programa começa com uma chave de substituição aleatória (alfabeto embaralhado).

Ele calcula o score (aptidão) do texto decifrado com essa chave.

Ele, então, entra em um loop: a. Faz uma pequena alteração na chave (troca duas letras aleatórias). b. Calcula o score do novo texto. c. Se o novo score for melhor que o anterior, ele mantém a nova chave. d. Se for pior, ele descarta a alteração.

Isso é repetido milhares de vezes, "subindo a colina" em direção ao score mais alto possível, que corresponde à mensagem legível.

3. A Métrica de Fitness (ngram_score.py)
Este é o "oráculo" do programa.

Ele carrega o arquivo quadgrams.txt, que contém uma lista de ~380.000 sequências de 4 letras (quad-grams) e sua frequência de ocorrência na língua inglesa.

Ele calcula a probabilidade logarítmica (log-probability) de um texto. A soma das log-probabilidades é usada para evitar underflow numérico (multiplicar números muito pequenos).

Textos com scores mais altos (menos negativos) são considerados mais parecidos com o inglês.

🗂️ Arquivos no Repositório
cesardesc.py: O script principal em Python com o menu interativo e os algoritmos de ataque.

encoded.txt: A mensagem criptografada, representada em binário ASCII.

ngram_score.py: Um script auxiliar (módulo) que implementa a classe ngram_score para calcular a aptidão do texto.

quadgrams.txt: O arquivo de dados (corpus) com as frequências dos quad-grams. É um arquivo grande.

⚙️ Como Usar
Pré-requisitos
Python 3.x

Não são necessárias bibliotecas externas.

Execução
Clone este repositório ou baixe todos os 4 arquivos.

Certifique-se de que todos os arquivos (cesardesc.py, encoded.txt, ngram_score.py, quadgrams.txt) estejam na mesma pasta.

Abra um terminal, navegue até a pasta do projeto e execute o script:

Bash

python cesardesc.py
O programa solicitará o nome do arquivo codificado. Digite:

encoded.txt
Aguarde alguns segundos enquanto o script carrega o arquivo quadgrams.txt na memória.

Use o menu interativo:

Digite 1 para executar o ataque rápido (e falho) da Cifra de César.

Digite 2 para executar o ataque de Substituição (Hill Climbing). Este processo levará alguns minutos e você verá o progresso no terminal à medida que ele encontra scores melhores.

Digite 3 para sair.
