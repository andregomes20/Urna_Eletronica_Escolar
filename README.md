<h1>🗳️ Urna Eletrônica Escolar - Sistema Digital</h1>

Este é um software de votação digital desenvolvido para facilitar eleições de Grêmio Estudantil, Representantes de Turma e Referendos Escolares. O sistema simula a interface de uma urna eletrônica real, garantindo segurança e facilidade de uso para os alunos.

<h2>👨‍💻 Sobre o Desenvolvedor</h2>

<p><b>Desenvolvedor:</b> Prof. André Eduardo Gomes</p>
<p><b>Contato/E-mail:</b> andre.gomes2004@gmail.com</p>
<p><b>Versão:</b> 3.0 (Windows) - 2025</p>

<h2>🚀 Como Instalar e Rodar</h2>

<b>Opção 1:</b> Arquivo Executável (.exe)

<ul>&bull; Se você recebeu o arquivo urna.exe:</ul>
<ul>&bull; Basta dar dois cliques no arquivo urna.exe.</ul>

<p><b>Nota:</b> Na primeira execução, o Windows pode exibir uma mensagem dizendo "O Windows protegeu o computador". Clique em Mais informações e depois em Executar assim mesmo.</p>

<p>O programa criará automaticamente uma <b>pasta assets_urna (para guardar fotos)</b> e um <b>arquivo dados_urna.json (para guardar os votos)</b> na mesma pasta onde ele estiver.</p>

<h2>⚙️ Área Administrativa (Configuração)</h2>

<p>Esta área é restrita aos professores ou responsáveis pela eleição.</p>

<p><b>Como Acessar:</b></p>
<p>Na tela inicial, clique no botão azul <b>"PAINEL ADMINISTRATIVO".</b></p>
<p>Digite a senha padrão: <b>admin</b></p>
<p>Clique em OK.</p>

<h3>Funcionalidades do Painel:</h3>

<h3>1. Aba "Geral & Modo"</h3>

<p><b>Título da Eleição:</b> Altere o nome que aparece no topo da urna (Ex: "Eleições 2025").</p>
<p><b>Modo de Votação:</b> Escolha entre:</p>
<p><b>Completo:</b> Vota para Chapa e depois responde as Perguntas.</p>
<p><b>Apenas Chapas:</b> Só eleição de candidatos.</p>
<p><b>Apenas Perguntas:</b> Só referendo (Sim/Não).</p>
<p><b>Logo da Escola:</b> Clique em "Escolher Arquivo" para colocar o brasão da sua escola na tela inicial e no PDF.</p>
<p><b>ZERAR VOTOS:</b> Botão vermelho de segurança. Apaga todos os votos e reinicia a eleição.</p>

<h3>2. Aba "Candidatos (Chapas)"</h3>

<p>Cadastre o Número e Nome dos candidatos.</p>
<p><b>Foto:</b> Você pode carregar uma foto (JPG/PNG) do computador.</p>
<p>Use o botão <b>"Adicionar"</b> para salvar e <b>"Remover Selecionado"</b> para excluir.</p>

<h3>3. Aba "Referendos (Perguntas)"</h3>

<p>Crie perguntas para a comunidade escolar (Ex: "Aprovar novo uniforme?").</p>
<p>Na hora de votar, aparecerão as opções: <b>1-SIM</b> e <b>2-NÃO.</b></p>

<h3>4. Aba "Resultados"</h3>

<p>Acompanhe a contagem de votos em tempo real na tela (com barras visuais).</p>

<p><b>Gerar Relatório PDF:</b> Gera um documento oficial </p>

<p><b>contendo:</b> Hora de Início e Término da votação.</p>
<p> - Total de votos.</p>
<p> - Vencedores ordenados por quantidade de votos.</b>
<p> - Gráficos e estatísticas de votos Brancos e Nulos.</p>

<h2>🗳️ Funcionalidades do Usuário (O Eleitor)</h2>

<p><b>Tela Inicial:</b> O aluno encontra uma tela de bloqueio. O mesário deve clicar em "INICIAR VOTAÇÃO" para liberar a urna.</p>
<p><b>Votação para Chapa:</b> O aluno digita o número do candidato no teclado virtual. Aparece a foto e o nome.</p>

<p>Botão <b>CORRIGE:</b> Limpa o número.</p>
<p>Botão <b>BRANCO:</b> Vota em branco.</p>
<p>Botão C<b>ONFIRMA:</b> Registra o voto (toca som característico se configurado).</p>

<p>Se digitar número inexistente ou <b>"00"</b>, o voto é computado como <b>NULO.</b></p>

<p><b>Votação para Referendo (se houver):</b></p>
<p><b>Botão SIM (1)</b> ou <b>NÃO (2).</b></p>

<p><b>Fim:</b> Aparece a palavra "FIM" gigante e a urna reinicia sozinha após 3 segundos, pronta para o próximo aluno.</p>

<h2>🔐 Comandos Secretos (Sair da Urna)</h2>

<p>Como a urna roda em tela cheia (modo quiosque) para evitar que alunos mexam no sistema, não há botão "Sair" na tela de votação.
Para voltar ao Menu Inicial ou Fechar o programa durante a votação:</p>

<p><b>Opção A (Teclado Físico):</b> Aperte a tecla <b>ESC</b> (Escape) no teclado do computador.</p>
<p><b>Opção B (Código Secreto):</b> Digite o número <b>99999</b> (cinco noves) no teclado numérico (da tela ou físico).</p>

<p>O sistema perguntará: <b>"Sair para o menu inicial?"</b>. Clique em Sim.</p>

<h2>📂 Arquivos Importantes</h2>

<p><b>urna.exe:</b> O programa principal.</p>

<p><b>dados_urna.json:</b> Arquivo onde os votos são salvos. Não apague este arquivo durante a eleição, ou perderá os votos.</p>
<p><b>assets_urna/:</b> Pasta onde ficam as fotos dos candidatos e o logo da escola.</p>
<p><b>Relatorio_Data_Hora.pdf:</b> Arquivo gerado ao clicar em <b>"Imprimir Resultado".</b></p>
