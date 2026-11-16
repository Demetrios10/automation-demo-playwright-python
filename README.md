# Cadastro Web · Python + Playwright

Portfólio de automação do [Automation Demo Site](https://demo.automationtesting.in/Register.html), com **Page Object Model**, cenários independentes e evidências por teste.

## O que é testado

- Dados pessoais e seleção exclusiva de gênero.
- Marcação e desmarcação de vários hobbies.
- E-mail, telefone, campos obrigatórios e regras de senha.
- Confirmação de senha divergente e senha válida.
- Upload de foto fictícia e limpeza pelo botão Refresh.
- Cadastro completo: dados, idiomas, habilidade, dois seletores de país, nascimento, senha, foto e envio.

**Importante:** o cenário completo exige que as listas e o serviço do site funcionem. Uma lista obrigatória vazia causa falha explícita, com evidência. Os testes não inserem opções no HTML, não simulam cadastro aprovado e não confundem preenchimento com persistência. A navegação para WebTable é o critério do fluxo demonstrativo; não comprova persistência no servidor.

## Executar no Windows / PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest
```

Para acompanhar no navegador:

```powershell
.\.venv\Scripts\python.exe -m pytest --headed --slowmo 150
```

Só o cadastro completo:

```powershell
.\.venv\Scripts\python.exe -m pytest -m complete --headed
```

Use Python 3.11 ou superior. Não é necessário ativar o ambiente virtual. No Linux/macOS, substitua o executável por `.venv/bin/python`.

## Organização

```text
pages/register_page.py     Seletores e ações do formulário
data/registration.py       Dados fictícios e e-mail único por execução
data/avatar.png            Imagem sintética para upload
tests/test_registration.py Cenários e expectativas
conftest.py                Fixtures e coleta automática de evidências
evidencias/                Resultados publicados e novas execuções
docs/                     Plano de testes e limitações
```

O Page Object cuida da interface; os testes descrevem as verificações. Cada cenário começa com um contexto limpo. O Playwright usa esperas automáticas, sem pausas fixas. Campos de senha são mascarados nas capturas.

## Evidências e resultado

Cada execução gera `evidencias/execucoes/<data-hora>/<cenario>/`, com capturas PNG e `resultado.json` contendo o estado real: aprovado, falhou ou ignorado. A data usa o fuso de São Paulo. Novas execuções ficam fora do Git para evitar crescimento acidental do repositório.

Veja o [resultado da validação inicial](docs/RESULTADOS.md) e o [plano de testes](docs/PLANO-DE-TESTES.md).

O fluxo do GitHub Actions é manual, para evitar acessos recorrentes desnecessários ao site público. Os resultados e capturas são anexados à execução mesmo quando há falhas.
