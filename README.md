# Aplicação de Agendamento e Confirmação via WhatsApp

Esta é uma aplicação de exemplo que permite agendar eventos e confirmar agendamentos via WhatsApp. A aplicação é projetada para ser agendada e executada automaticamente usando o Google Scheduler.

## Funcionalidades

- Recebe dados de agendamento via uma rota HTTP.
- Agenda o envio de mensagens de confirmação via WhatsApp para os participantes do evento.
- Lida com respostas dos participantes e toma ações com base nas respostas (confirmação ou cancelamento).
- Envia mensagens de remarcação em caso de cancelamento.
- Atualiza o status do agendamento via requisição HTTP POST.


## Configuração

1. Clone este repositório para o seu ambiente local.

2. Personalize a aplicação conforme suas necessidades:
   - Defina as mensagens, URLs e a lógica de atualização do status do agendamento.

3. Implante a aplicação em um servidor da sua escolha. Certifique-se de configurar as variáveis de ambiente necessárias, como chaves de API, se aplicável.

4. Configure o Google Scheduler para agendar a execução da aplicação de acordo com o seu cronograma. Você pode usar uma tarefa de agendamento para enviar os dados de agendamento para a rota `/receber_agendamento` da sua aplicação.

## Uso

- Execute a aplicação em um servidor acessível pela Internet.

- Agende a execução da aplicação usando o Google Scheduler ou outra ferramenta de agendamento de tarefas.

- A aplicação lidará com o agendamento de mensagens e as respostas dos participantes automaticamente.


