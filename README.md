🗳️ Urna Eletrônica Escolar - Sistema Digital

Este é um software de votação digital desenvolvido para facilitar eleições de Grêmio Estudantil, Representantes de Turma e Referendos Escolares. O sistema simula a interface de uma urna eletrônica real, garantindo segurança e facilidade de uso para os alunos.

👨‍💻 Sobre o Desenvolvedor

Desenvolvedor: Prof. André Eduardo Gomes
Contato/E-mail: andregomes20@gmail.com
Versão: 3.0 (Windows)

🚀 Como Instalar e Rodar

Opção 1: Arquivo Executável (.exe)

Se você recebeu o arquivo urna.exe:
Basta dar dois cliques no arquivo urna.exe.

Nota: Na primeira execução, o Windows pode exibir uma mensagem dizendo "O Windows protegeu o computador". Clique em Mais informações e depois em Executar assim mesmo.

O programa criará automaticamente uma pasta assets_urna (para guardar fotos) e um arquivo dados_urna.json (para guardar os votos) na mesma pasta onde ele estiver.

⚙️ Área Administrativa (Configuração)

Esta área é restrita aos professores ou responsáveis pela eleição.

Como Acessar:
Na tela inicial, clique no botão azul "PAINEL ADMINISTRATIVO".
Digite a senha padrão: admin
Clique em OK.
Funcionalidades do Painel:

1. Aba "Geral & Modo"

Título da Eleição: Altere o nome que aparece no topo da urna (Ex: "Eleições 2025").
Modo de Votação: Escolha entre:
Completo: Vota para Chapa e depois responde as Perguntas.
Apenas Chapas: Só eleição de candidatos.
Apenas Perguntas: Só referendo (Sim/Não).
Logo da Escola: Clique em "Escolher Arquivo" para colocar o brasão da sua escola na tela inicial e no PDF.
ZERAR VOTOS: Botão vermelho de segurança. Apaga todos os votos e reinicia a eleição.

2. Aba "Candidatos (Chapas)"

Cadastre o Número e Nome dos candidatos.
Foto: Você pode carregar uma foto (JPG/PNG) do computador.
Use o botão "Adicionar" para salvar e "Remover Selecionado" para excluir.

3. Aba "Referendos (Perguntas)"

Crie perguntas para a comunidade escolar (Ex: "Aprovar novo uniforme?").
Na hora de votar, aparecerão as opções: 1-SIM e 2-NÃO.

4. Aba "Resultados"

Acompanhe a contagem de votos em tempo real na tela (com barras visuais).

Gerar Relatório PDF: Gera um documento oficial contendo:
Hora de Início e Término da votação.
Total de votos.
Vencedores ordenados por quantidade de votos.
Gráficos e estatísticas de votos Brancos e Nulos.

🗳️ Funcionalidades do Usuário (O Eleitor)

Tela Inicial: O aluno encontra uma tela de bloqueio. O mesário deve clicar em "INICIAR VOTAÇÃO" para liberar a urna.
Votação para Chapa: O aluno digita o número do candidato no teclado virtual. Aparece a foto e o nome.

Botão CORRIGE: Limpa o número.
Botão BRANCO: Vota em branco.
Botão CONFIRMA: Registra o voto (toca som característico se configurado).

Se digitar número inexistente ou "00", o voto é computado como NULO.

Votação para Referendo (se houver):
Botão SIM (1) ou NÃO (2).

Fim: Aparece a palavra "FIM" gigante e a urna reinicia sozinha após 3 segundos, pronta para o próximo aluno.

🔐 Comandos Secretos (Sair da Urna)

Como a urna roda em tela cheia (modo quiosque) para evitar que alunos mexam no sistema, não há botão "Sair" na tela de votação.
Para voltar ao Menu Inicial ou Fechar o programa durante a votação:

Opção A (Teclado Físico): Aperte a tecla ESC (Escape) no teclado do computador.
Opção B (Código Secreto): Digite o número 99999 (cinco noves) no teclado numérico (da tela ou físico).

O sistema perguntará: "Sair para o menu inicial?". Clique em Sim.

📂 Arquivos Importantes

urna.exe: O programa principal.

dados_urna.json: Arquivo onde os votos são salvos. Não apague este arquivo durante a eleição, ou perderá os votos.
assets_urna/: Pasta onde ficam as fotos dos candidatos e o logo da escola.
Relatorio_Data_Hora.pdf: Arquivo gerado ao clicar em "Imprimir Resultado".
