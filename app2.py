import json
import pywhatkit as kit
from datetime import datetime, timedelta
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def enviar_mensagem_whatsapp(destinatario, mensagem, hora, minuto):
    kit.sendwhatmsg(destinatario, mensagem, hora, minuto)

def enviar_mensagem_remarcacao(destinatario):
    mensagem = "Lamentamos o cancelamento. Deseja remarcar o evento? Responda 'Sim' ou 'Não'."
    kit.sendwhatmsg(destinatario, mensagem, hora, minuto)

def atualizar_status_agendamento(id_agendamento, novo_status):
    try:
        import requests
        url = 'https://sua-api.com/atualizar_status_agendamento'
        dados = {
            'id_agendamento': id_agendamento,
            'novo_status': novo_status
        }
        resposta = requests.post(url, json=dados)
        if resposta.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro ao atualizar o status do agendamento: {str(e)}")
        return False

def coletar_informacoes():
    try:
        # Substitua esta URL pela URL da sua API
        api_url = 'https://sua-api.com/obter_informacoes_agendamento'
        response = requests.get(api_url)

        if response.status_code == 200:
            agendamentos = response.json()
            agora = datetime.now()

            for agendamento in agendamentos:
                data_agendamento = datetime.strptime(agendamento['data'], '%Y-%m-%d %H:%M:%S')
                if (data_agendamento - timedelta(days=1)) == agora:
                    enviar_mensagem_whatsapp(agendamento['destinatario'], agendamento['evento'], data_agendamento)

    except Exception as e:
        print(f"Erro ao coletar informações do agendamento: {str(e)}")

@app.route('/receber_agendamento', methods=['POST'])
def receber_agendamento():
    try:
        agendamento_json = request.get_json()
        if 'destinatario_whatsapp' in agendamento_json and 'evento' in agendamento_json and 'data' in agendamento_json:
            destinatario = agendamento_json['destinatario_whatsapp']
            evento = agendamento_json['evento']
            data = agendamento_json['data']
            agora = datetime.now()
            hora_envio = agora + timedelta(minutes=5)
            mensagem = f"Você tem um evento agendado: {evento} em {data}. Responda 'Sim' para confirmar ou 'Não' para cancelar."
            enviar_mensagem_whatsapp(destinatario, mensagem, hora_envio.hour, hora_envio.minute)
            return jsonify({'mensagem': 'Mensagem de confirmação agendada para envio em 5 minutos'})
        else:
            return jsonify({'erro': 'Dados de agendamento incompletos'})
    except Exception as e:
        return jsonify({'erro': str(e)})

@app.route('/receber_resposta', methods=['POST'])
def receber_resposta():
    try:
        resposta_json = request.get_json()
        if 'destinatario_whatsapp' in resposta_json and 'resposta' in resposta_json:
            destinatario = resposta_json['destinatario_whatsapp']
            resposta = resposta_json['resposta']
            if resposta.lower() == 'sim':
                mensagem = "Agradecemos pela confirmação. Estamos aguardando você no evento!"
                kit.sendwhatmsg(destinatario, mensagem, hora, minuto)
            elif resposta.lower() == 'nao':
                enviar_mensagem_remarcacao(destinatario)
                sucesso = atualizar_status_agendamento(resposta_json['id_agendamento'], 'cancel')
                if sucesso:
                    print("Status do agendamento atualizado com sucesso.")
                else:
                    print("Falha ao atualizar o status do agendamento.")
            return jsonify({'mensagem': 'Resposta do cliente processada'})
        else:
            return jsonify({'erro': 'Dados de resposta incompletos'})
    except Exception as e:
        return jsonify({'erro': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
