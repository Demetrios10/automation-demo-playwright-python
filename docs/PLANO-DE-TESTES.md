# Plano de testes

Ambiente: https://demo.automationtesting.in/Register.html

| Grupo | Verificação |
| --- | --- |
| Disponibilidade | Formulário e botão de envio visíveis |
| Identidade | Nome, sobrenome, endereço, e-mail, telefone e gênero |
| Gênero | Masculino e feminino, mantendo apenas uma opção selecionada |
| Hobbies | Seleção múltipla e desmarcação |
| E-mail | Três formatos inválidos |
| Telefone | Curto, longo e letras: padrão de dez dígitos da página |
| Obrigatoriedade | Envio vazio bloqueado pela validação HTML |
| Senha | Complexidade ausente, confirmação divergente e par válido |
| Foto | Arquivo PNG selecionado e prévia carregada |
| Refresh | Limpa os dados preenchidos |
| Completo | Preenche todos os componentes e envia; aguarda WebTable |

Dados inteiramente fictícios: domínio example.com, endereço de teste e avatar sintético. Nenhum dado do titular do GitHub é enviado ao formulário.

O teste completo falha se o site não fornecer habilidade, país obrigatório ou ano necessários. Isto identifica dependência indisponível; não deve ser alterado para aprovação artificial. Nenhum teste faz mock de rede ou altera opções do DOM.

Limites: não cobre todos os navegadores, acessibilidade, desempenho, persistência ou segurança. Mensagens são avaliadas conforme a implementação do site, sem afirmar que suas regras representam um cadastro de produção.
