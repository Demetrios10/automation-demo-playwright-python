# Problemas observados no site

## CAD-001 · País obrigatório sem opções

1. Abrir o formulário e preencher os dados pessoais.
2. Selecionar hobbies, idiomas, habilidade, nascimento e o país no componente de busca.
3. Verificar o campo obrigatório **Country**, que é diferente de **Select Country**.

Esperado: opções válidas disponíveis para preencher o campo obrigatório e enviar o formulário.

Observado: o seletor `#countries` oferece somente o item vazio “Select Country”. O segundo seletor (`#country`) funciona, mas não preenche o primeiro.

Impacto: o cadastro completo não pode avançar. O cenário `test_cadastro_completo` falha com `SiteDependencyError`, preservando a tela preenchida e a descrição da dependência. O teste não modifica a página para contornar a validação.

## CAD-002 · Foto selecionada sem prévia

1. Abrir o formulário.
2. Selecionar o arquivo sintético `data/avatar.png` no campo Photo.

Esperado: a imagem de prévia refletir o arquivo escolhido.

Observado: o campo recebe um arquivo, mas `#imagetrgt` continua apontando para `original.png`.

Impacto: falha na prévia da foto. A seleção do arquivo é verificada por um teste separado e pode passar enquanto a prévia falha.

Estas observações se referem à execução histórica documentada em [RESULTADOS.md](RESULTADOS.md). Uma correção no site deve ser verificada por nova execução, sem alterar as expectativas para produzir aprovação artificial.
