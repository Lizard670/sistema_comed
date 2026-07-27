# Relatório de Testes de Sistema

## 1. Objetivo
Este relatório registra os testes realizados para verificar e validar as funcionalidades do sistema, garantindo que os requisitos funcionais sejam atendidos.

## 2. Ambiente de Testes

| Item | Descrição |
| :--- | :--- |
| **Sistema Operacional** | Windows 11 |
| **Banco de Dados** |  |
| **Linguagem** | Python |
| **Versão do Sistema** | 3.14 |

 **Códigos usados** 

![cod01](static\assets\img\usuario-model.png)
![cod02 ](static\assets\img\alunomodel.png)
![cod03](static\assets\img\curso-turma.png)

## 3. Casos de Teste

| ID | Requisito | Procedimento | Resultado Esperado | Resultado Obtido | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **CT-01** | Cadastrar estudantes | Verificar se o sistema permite cadastrar novos estudantes. | Cadastro realizado com sucesso. Dados armazenados corretamente no banco. | O cadastro foi concluído normalmente. As informações ficaram disponíveis para consulta. | **Aprovado** |
| **CT-02** | Registrar atendimentos | Verificar o registro de atendimentos contendo data, descrição e status. | O sistema deve salvar todas as informações informadas. | Os registros foram salvos corretamente. Foi possível visualizar posteriormente os atendimentos cadastrados. | **Aprovado** |
| **CT-03** | Atualizar e acompanhar atendimentos | Verificar se é possível alterar o status de um atendimento. | Alterações devem ser salvas imediatamente. | O status foi atualizado corretamente e refletido no histórico. | **Aprovado** |
| **CT-04** | Gerar histórico individual | Verificar se o sistema apresenta todo o histórico do estudante. | Exibir todos os atendimentos relacionados ao estudante. | O histórico foi exibido em ordem cronológica contendo todas as informações registradas. | **Aprovado** |
| **CT-05** | Emitir atestados digitais (PDF) | Validar a geração do PDF e do código único. | PDF gerado corretamente. Código único diferente para cada documento. | O PDF foi criado sem erros. Cada documento apresentou um código exclusivo para validação. | **Aprovado** |
| **CT-06** | Disponibilizar relatórios gerenciais | Verificar a geração dos relatórios institucionais. | Relatórios contendo dados atualizados dos atendimentos. |  | **-** |

---

## Validação 1 – Registro de Atendimentos

*   **Objetivo:** Validar se o processo de registro de atendimentos atende às necessidades dos usuários.
*   **Procedimento realizado:** O sistema foi utilizado para registrar diversos atendimentos simulando o uso por um servidor responsável pelo atendimento estudantil.
*   **Resultado esperado:** O usuário deve conseguir registrar um atendimento de forma rápida, visualizar seu status e acompanhar sua evolução.
*   **Resultado obtido:** O usuário conseguiu registrar atendimentos sem dificuldades, alterar o status quando necessário e acompanhar todas as atualizações realizadas.
*   **Conclusão:** A funcionalidade atende às necessidades do usuário final e facilita o controle dos atendimentos.
*   **Status:**  **Validado**
*   **Anexos:**![pagina01](static\assets\img\addestudante.png)

---

## Validação 2 – Relatórios Gerenciais

*   **Objetivo:** Validar se os relatórios fornecem informações úteis para o usuário.
*   **Procedimento realizado:** Foram gerados relatórios contendo dados de estudantes e atendimentos cadastrados no sistema.
*   **Resultado esperado:** Os relatórios devem apresentar informações claras que auxiliem no acompanhamento institucional e na tomada de decisões.
*   **Resultado obtido:** 
*   **Conclusão:** 
*   **Status:**  **-**   