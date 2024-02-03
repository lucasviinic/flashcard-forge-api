# Flashcard Forge API

### Sobre

Um projeto para gerar flashcards a partir de PDFs e grandes conjuntos de dados de texto usando inteligência artificial generativa.

### Motivação

Uma das abordagens mais eficazes para a aprendizagem e retenção de conteúdo durante os estudos é a utilização de flashcards.
Essa estratégia envolve o uso de pequenos cartões contendo uma pergunta de um lado e a resposta correspondente do outro. No entanto,
um dos maiores desafios para aqueles que adotam essa estratégia é a criação das perguntas e suas respectivas respostas.
Em cenários mais desafiadores, como ao lidar com um capítulo extenso sobre genética, essa tarefa pode consumir um tempo considerável e valioso.
Diante desse desafio, dei início a este projeto para auxiliar aqueles na jornada massiva de estudos, espero estar ajudando um pouco.

### Status

**Step 00: Prova de conceito**
- [x] Desenvolvimento e teste de módulo processador de PDFs (extração de textos de diversos tipos de PDF).
- [x] Desenvolvimento e teste de geração de flashcards com base em grandes quantidades de texto.

**Considerações finais:** Diversas abordagens foram investigadas para a extração de texto de PDFs, abrangendo inclusive PDFs que contêm imagens
e tabelas. No entanto, por ora, optou-se por excluir a implementação desses dois últimos elementos, reservando-os para
futuras atualizações. A criação de um módulo especializado para a extração de texto de imagem, o chamado OCR (Optical Character Recognition)
e tabelas é essencial, mas, neste momento, a obtenção de texto atende satisfatoriamente a maioria dos casos, podendo seguir adiante.
      
**Step 01: Setup e implementação do core**
- [x] Definir arquitetura e setups iniciais
- [x] Implementação do core e serviços auxiliares (integração com a OpenAI e funções para processamento de PDF)
- [x] Desenvolvimento de usecase para criação de flashcards
- [x] Desenvolvimento do endpoint de criação de flashcards

**Considerações finais:** O propósito desta fase foi traduzir para a API o que foi previamente planejado e testado na etapa de prova de conceito. Nesse sentido, foi desenvolvido o endpoint responsável por gerar os flashcards, que constitui o cerne do projeto. Com essa etapa concluída, torna-se viável avançar para a definição de todas as entidades da aplicação, incluindo aquelas relacionadas aos usuários, aos próprios flashcards e demais elementos que interagirão em conjunto.

**Step 02: Definição das entidades, modelagem das tabelas e setup do banco de dados (Previsão)**

- [ ] Diagrama ER do banco de dados
- [ ] Criação dos models (entidades) da API
- [ ] Migrations

**Step 03: Autenticação e Autorização (Previsão)**

- [ ] Endpoint de criação de usuário
- [ ] Hash de senha do usuário
- [ ] Autenticação do usuário

**Step 04: Planning** <img src="https://media.tenor.com/On7kvXhzml4AAAAj/loading-gif.gif" width="15" height="15" style="vertical-align: middle;">












