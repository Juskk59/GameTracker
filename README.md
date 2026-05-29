# GameTracker 🎮

Aplicação desktop desenvolvida em **Python** para organizar uma biblioteca pessoal de jogos avaliados.

O **GameTracker** permite que usuários criem uma conta, façam login e mantenham sua própria coleção de jogos, cadastrando títulos, plataformas, notas, descrições e imagens de capa. O sistema também apresenta estatísticas simples da biblioteca, como a quantidade total de jogos avaliados e a média das notas registradas.

## Funcionalidades

### Autenticação de usuários

- Cadastro de novos usuários;
- Login utilizando e-mail e senha;
- Validação de e-mail já cadastrado;
- Biblioteca individual vinculada ao usuário autenticado;
- Logout da aplicação.

### Biblioteca de jogos

- Cadastro de novos jogos;
- Listagem dos jogos adicionados pelo usuário;
- Edição das informações de um jogo;
- Exclusão de jogos da biblioteca;
- Associação dos jogos ao usuário responsável pelo cadastro.

### Avaliações e informações dos jogos

Cada jogo pode armazenar:

- Título;
- Plataforma;
- Nota de `0` a `10`;
- Descrição;
- Imagem de capa.

### Imagens de capa

- Seleção de imagem para representar o jogo;
- Exibição da capa na biblioteca;
- Uso de placeholder quando nenhuma imagem é cadastrada;
- Conversão da imagem para Base64 para armazenamento no banco de dados.

### Estatísticas

O painel principal apresenta:

- Número total de jogos avaliados;
- Nota média dos jogos cadastrados pelo usuário.

### Conteúdo inicial

No primeiro login de um novo usuário, o sistema adiciona automaticamente três jogos de exemplo à biblioteca:

- The Last of Us Part I;
- Elden Ring;
- Zelda: Tears of the Kingdom.

## Tecnologias utilizadas

- **Python** — linguagem principal da aplicação;
- **Tkinter** — construção da interface gráfica desktop;
- **MongoDB** — banco de dados NoSQL utilizado para persistência;
- **PyMongo** — integração entre Python e MongoDB;
- **Pillow (PIL)** — carregamento, redimensionamento e exibição das imagens;
- **BSON / ObjectId** — identificação e relacionamento dos documentos no MongoDB;
- **Base64** — armazenamento das imagens dos jogos no banco de dados.

## Arquitetura do projeto

O projeto foi estruturado seguindo o padrão **MVC (Model-View-Controller)**, separando a interface gráfica, as regras de controle e a persistência dos dados.

```text
GameTracker/
├── assets/
│   └── imagens/                  # Imagens utilizadas ou salvas pela aplicação
├── controller/
│   └── gametracker_controller.py # Comunicação entre View e Models
├── models/
│   ├── jogo.py                   # Regras e persistência dos jogos
│   └── usuario.py                # Cadastro e autenticação dos usuários
├── view/
│   └── gametracker_view.py       # Interface gráfica da aplicação
└── main.py                       # Inicialização do sistema
```

## Responsabilidade dos arquivos

### `main.py`

Arquivo principal da aplicação. Ele:

- Inicializa o controller;
- Verifica a conexão com o MongoDB;
- Cria a interface gráfica;
- Inicia o loop principal da aplicação.

### `controller/gametracker_controller.py`

Camada intermediária entre a interface e os models. É responsável por ações como:

- Realizar login;
- Cadastrar usuários;
- Adicionar jogos;
- Editar jogos existentes;
- Excluir jogos;
- Listar os jogos do usuário;
- Obter estatísticas da biblioteca;
- Processar imagens selecionadas.

### `models/usuario.py`

Model responsável pelos usuários da aplicação. Implementa:

- Cadastro de novos usuários;
- Verificação de e-mail já existente;
- Autenticação por e-mail e senha;
- Criação automática de jogos de exemplo no primeiro acesso.

### `models/jogo.py`

Model responsável pelos jogos armazenados na biblioteca. Implementa:

- Cadastro de jogos;
- Atualização de registros;
- Exclusão;
- Busca dos jogos por usuário;
- Cálculo de estatísticas;
- Conversão de imagens para Base64;
- Salvamento local de imagens na pasta de assets.

### `view/gametracker_view.py`

Camada visual do sistema, desenvolvida com Tkinter. Contém:

- Tela de login;
- Tela de cadastro;
- Dashboard da biblioteca;
- Cards dos jogos cadastrados;
- Painel de estatísticas;
- Formulários para adicionar e editar jogos;
- Exibição das imagens de capa;
- Botões de navegação e logout.

## Plataformas disponíveis

Ao cadastrar um jogo, o sistema disponibiliza as seguintes opções de plataforma:

- PlayStation 5;
- PlayStation 4;
- Xbox Series X/S;
- Xbox One;
- Nintendo Switch;
- PC;
- Mobile.

## Banco de dados

A aplicação utiliza o MongoDB local com a seguinte configuração:

```text
Conexão: mongodb://localhost:27017/
Banco: gametracker_db
```

As coleções utilizadas são:

```text
usuarios
jogos
```

### Estrutura aproximada dos usuários

```json
{
  "nome": "Nome do usuário",
  "email": "usuario@email.com",
  "senha": "senha"
}
```

### Estrutura aproximada dos jogos

```json
{
  "titulo": "Elden Ring",
  "plataforma": "PC",
  "nota": 9.0,
  "descricao": "Descrição ou avaliação do jogo.",
  "id_user": "ObjectId do usuário",
  "imagem_jogo": "Imagem convertida para Base64"
}
```

## Pré-requisitos

Antes de executar o projeto, tenha instalado:

- **Python 3**;
- **MongoDB Community Server** ou uma instância MongoDB disponível localmente.

A aplicação espera que o MongoDB esteja executando em:

```text
localhost:27017
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Juskk59/GameTracker.git
```

Acesse a pasta do projeto:

```bash
cd GameTracker
```

Instale as dependências necessárias:

```bash
pip install pymongo pillow
```

Certifique-se de que o MongoDB esteja iniciado antes de executar a aplicação.

## Como executar

Na raiz do projeto, execute:

```bash
python main.py
```

Caso a conexão com o MongoDB não esteja disponível, o sistema exibirá uma mensagem informando que não foi possível acessar o banco local.

## Como utilizar

### Criar uma conta

1. Abra a aplicação.
2. Na tela inicial, acesse a opção de cadastro.
3. Informe seu nome, e-mail e senha.
4. Confirme o cadastro.
5. Volte para a tela de login.

### Fazer login

1. Informe o e-mail cadastrado.
2. Digite sua senha.
3. Entre no sistema.
4. No primeiro login, alguns jogos de exemplo serão inseridos automaticamente na biblioteca.

### Adicionar um jogo

1. No dashboard, clique em **Adicionar novo Jogo**.
2. Preencha as informações:
   - Título;
   - Plataforma;
   - Nota;
   - Descrição.
3. Selecione uma imagem de capa, caso desejado.
4. Salve o registro.

### Visualizar a biblioteca

Após o login, os jogos cadastrados são exibidos em cards contendo suas informações e imagens de capa. Caso um jogo não possua imagem, a aplicação utiliza um placeholder visual.

### Editar um jogo

1. Selecione a opção de edição no card desejado.
2. Atualize título, plataforma, nota, descrição ou imagem.
3. Salve as alterações.

### Excluir um jogo

1. Selecione a opção de remoção do jogo desejado.
2. Confirme a exclusão.
3. O registro será removido da sua biblioteca.

## Conceitos aplicados

Este projeto explora conceitos importantes de desenvolvimento de software:

- Desenvolvimento de aplicações desktop com interface gráfica;
- Arquitetura MVC;
- Persistência de dados com banco NoSQL;
- Operações CRUD;
- Cadastro e autenticação de usuários;
- Relacionamento entre documentos utilizando `ObjectId`;
- Manipulação e exibição de imagens;
- Armazenamento de imagens em Base64;
- Cálculo de estatísticas a partir de dados cadastrados.

## Observação sobre segurança

O projeto possui finalidade acadêmica e implementa uma autenticação simples. Atualmente, as senhas são armazenadas diretamente no MongoDB.

Para utilização em um ambiente real, seriam necessárias melhorias como:

- Armazenamento seguro de senhas utilizando hash;
- Validação mais completa dos dados;
- Controle de sessões;
- Tratamento avançado de exceções;
- Proteção das configurações de banco de dados;
- Otimização do armazenamento das imagens.

## Melhorias futuras

Algumas possíveis evoluções para o projeto:

- Implementar hash seguro para as senhas;
- Criar filtros por plataforma e nota;
- Adicionar busca por título;
- Permitir ordenar jogos por avaliação;
- Incluir status como jogando, finalizado ou desejado;
- Adicionar gêneros e data de lançamento;
- Criar ranking dos jogos mais bem avaliados;
- Melhorar o layout responsivo da interface;
- Armazenar apenas os caminhos das imagens em vez do conteúdo Base64;
- Criar um arquivo `requirements.txt`;
- Adicionar testes automatizados.

## Objetivo acadêmico

O **GameTracker** foi desenvolvido como projeto acadêmico com o objetivo de praticar a criação de uma aplicação desktop completa em Python, integrando interface gráfica, banco de dados, autenticação, operações CRUD e organização de código utilizando o padrão MVC.

## Autor

Desenvolvido por **Julio** como projeto acadêmico.
