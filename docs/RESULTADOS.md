# Resultado da validação inicial

Execução real em **15/11/2026**, Chromium headless no Windows, Python 3.14, Playwright 1.61.0 e pytest 8.4.2.

**22 cenários: 20 aprovados, 2 falharam, nenhum ignorado. Duração: 68,40 segundos.**

As falhas foram preservadas:

| Cenário | Resultado observado |
| --- | --- |
| `test_cadastro_completo` | O site não oferece opções no campo obrigatório `Country`; o fluxo para antes do envio, com `SiteDependencyError` |
| `test_previa_da_foto` | O arquivo é selecionado, mas a prévia permanece em `original.png` |

Os demais cenários passaram, incluindo os dois gêneros, três e-mails inválidos, três telefones inválidos, dados pessoais, hobbies, idiomas, país com busca, nascimento, senhas, obrigatoriedade, seleção do arquivo e Refresh.

O envio bem-sucedido do cadastro **não foi comprovado**, pois depende da correção do país obrigatório no site. O código do envio e sua expectativa de navegação estão implementados. Nenhuma lista foi alterada e nenhuma resposta de sucesso foi simulada.

Veja [os problemas reproduzidos](DEFEITOS.md), o [relatório JUnit](../evidencias/junit.xml) e as [capturas e resultados por cenário](../evidencias/validacao-inicial/). Há 23 capturas PNG e 22 arquivos JSON, com as senhas mascaradas.

Verificação de código: Ruff e Black sem pendências. O resultado é histórico; o workflow manual pode apresentar resultados diferentes conforme o estado do site.
