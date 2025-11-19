# Regras de Proteção de Branch

Este documento descreve as regras de proteção de branch configuradas para este repositório.

## Proteção do Branch Master

O branch `master` está protegido com as seguintes regras:

### ✅ Revisões Obrigatórias
- **Revisões de Pull Request são obrigatórias** antes do merge
- **Pelo menos 1 aprovação obrigatória** dos code owners
- Aprovação do code owner é **obrigatória** (veja o arquivo CODEOWNERS)

### ✅ Code Owners
Todas as alterações em qualquer arquivo no repositório requerem aprovação de **@Roteus**.

Veja o arquivo [CODEOWNERS](CODEOWNERS) para a lista completa de code owners.

## Como Contribuir

1. **Faça um fork do repositório** ou crie um novo branch
2. **Faça suas alterações** no seu branch
3. **Faça push do seu branch** para o GitHub
4. **Abra um Pull Request** para o branch `master`
5. **Aguarde revisão e aprovação** de @Roteus
6. Uma vez aprovado, o PR pode ser mergeado

## Configurando a Proteção de Branch no GitHub

Para garantir que essas regras sejam aplicadas, configure as seguintes opções no repositório do GitHub:

### Passos para Configurar:

1. Vá para **Settings** (Configurações) do repositório
2. Navegue até **Branches** (em "Code and automation")
3. Clique em **Add branch protection rule** (Adicionar regra de proteção de branch)
4. Em **Branch name pattern**, digite: `master`
5. Ative as seguintes opções:
   - ✅ **Require a pull request before merging** (Exigir pull request antes do merge)
     - ✅ Require approvals: **1** (Exigir aprovações: 1)
     - ✅ Dismiss stale pull request approvals when new commits are pushed (Descartar aprovações antigas quando novos commits forem enviados)
     - ✅ Require review from Code Owners (Exigir revisão dos Code Owners)
   - ✅ **Require status checks to pass before merging** (opcional, se você tiver CI/CD)
   - ✅ **Require branches to be up to date before merging** (Exigir que branches estejam atualizados antes do merge)
   - ✅ **Do not allow bypassing the above settings** (Não permitir ignorar as configurações acima) - recomendado
   - ✅ **Restrict who can push to matching branches** (opcional, para segurança adicional)
6. Clique em **Create** ou **Save changes**

### Recomendações Adicionais:

- **Include administrators**: Considere não permitir que administradores ignorem essas regras para máxima segurança
- **Require linear history**: Force um histórico de commits limpo exigindo histórico linear
- **Lock branch**: Previna qualquer push direto (todos devem usar Pull Requests)

## Por Que Essas Regras?

As regras de proteção de branch ajudam a manter a qualidade do código e garantem:
- Todas as alterações são revisadas antes do merge
- Nenhuma alteração acidental ou não autorizada no branch principal
- Melhor colaboração através do processo de revisão de PR
- Rastreabilidade de todas as alterações através do histórico de PR

## Dúvidas?

Se você tiver dúvidas sobre essas regras ou precisar de ajuda para criar um Pull Request, por favor abra uma issue ou contate @Roteus.
