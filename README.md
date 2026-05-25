# Jogo-da-Barbie
pygames jogo da barbie- Mariana Giacometti, Joana Gregorin, Laura Monteiro

**Título**: Barbie Shopping Rush
**Integrantes**: Laura Monteiro, Mariana Giacometti e Joana Gregorin

**Descrição do jogo**:
Barbie Shopping Rush é um animado jogo de sobrevivência temático, onde a Barbie precisa coletar o máximo de itens de moda enquanto desvia de nuvens cinzas que tentam atrapalhar sua sessão de compras. O jogador controla a Barbie em um cenário colorido e cheio de estilo, coletando bolsas, batons, sapatos, joias e coroas que caem pela tela, cada um valendo uma quantidade diferente de pontos.
O objetivo é simples: coletar o maior número possível de itens e sobreviver às ondas progressivamente mais difíceis. A cada rodada concluída, mais itens e mais nuvens surgem, tornando o desafio cada vez mais intenso. Durante a partida, power-ups aparecem pelo cenário oferecendo vantagens temporárias, como restauração de vida, escudo de imunidade, aumento de velocidade, imã que atrai itens e até uma estrela especial que elimina todos os obstáculos em tela de uma vez. O jogo só termina quando a barra de vida se esgota sem que haja vidas extras disponíveis, por isso cada decisão conta.
Não há um fim definido — a partida continua até a Barbie sucumbir. Acumule o máximo de pontos possível para garantir seu lugar no ranking das fashionistas!

**Como rodar o jogo**:
Abrir o repositório do GitHub no VsCode;
Após a abertura do repositório, baixar todos os arquivos presentes nele;
Em seguida, navegar até a pasta do projeto e abrir o arquivo main.py;
Para inicializar o jogo, pressionar o botão "Run" no canto superior direito da tela.


**Como jogar**:
Ao rodar o jogo, você verá a tela inicial, que conta com o título "Barbie Shopping Spree" ao centro, além de três botões:

"JOGAR": redireciona para a tela de inserção de nome, onde você digita seu nome (até 15 caracteres) e clica em "COMEÇAR" ou pressiona Enter para iniciar uma nova partida.
"RANKING": abre uma nova tela exibindo as 10 melhores pontuações já registradas, com os nomes das jogadoras. Um botão "VOLTAR" no rodapé retorna ao menu principal.
"SAIR": encerra o jogo.

Uma vez na partida, a tela exibe: uma barra de vida no canto superior esquerdo; a pontuação atual e o número da onda no canto superior direito; corações no rodapé representando as vidas extras disponíveis; e no restante da tela, a Barbie, os itens caindo e as nuvens perseguindo.
Os comandos de movimento são:

W ou ↑ — mover para cima
S ou ↓ — mover para baixo
A ou ← — mover para a esquerda
D ou → — mover para a direita


Para coletar itens e pegar power-ups, basta mover a Barbie até encostar neles — o efeito é ativado automaticamente.
Cada vez que uma nuvem cinza tocar a Barbie, ela sofrerá dano. Quando a barra de vida se esgotar sem vidas extras disponíveis, o jogo termina e a jogadora é redirecionada para a tela de Game Over, onde sua pontuação é exibida e salva automaticamente no ranking caso esteja entre as 10 maiores. É possível jogar novamente ou voltar ao menu principal.


**Instalação de Bibliotecas**:
**Pygame**:
Pré-requisitos: ter o VsCode e o Anaconda Prompt instalados;
Abrir o Anaconda Prompt e digitar: pip install pygame
No arquivo do projeto, utilizar: import pygame

**Demais**
Todas as outras bibliotecas utilizadas (math, random, json, os) já fazem parte da biblioteca padrão do Python, bastando importá-las com import nome_da_biblioteca.


**Uso de IA Generativa no Código**:

As linhas referentes às funções carregar_ranking, salvar_ranking e adicionar_ao_ranking foram desenvolvidas com auxílio de IA Generativa.

Explicação do material gerado por IA: As funções implementam um sistema de ranking que armazena nomes e pontuações em um arquivo JSON. carregar_ranking() verifica se o arquivo ranking.json existe e o carrega; caso não exista ou ocorra erro na leitura, retorna uma lista vazia. salvar_ranking(ranking) grava a lista atualizada de volta no arquivo. adicionar_ao_ranking(nome, score) insere um novo resultado, ordena a lista de forma decrescente pela pontuação, mantém apenas os 10 melhores e salva o ranking atualizado, retornando a lista final.

Além disso a IA sempre foi usada para fazer correções no código.

Algumas imagens utilizadas no jogo são provenientes de IA generativa.

**Endereço Vídeo do Jogo:**
