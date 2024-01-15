import tornado.ioloop
import tornado.web
import json
import random
import string

from ..base import BaseHandlerUser
from ..base import RequestPasswordResetHandler

# Simulando um banco de dados de usuários
users = {
    "user1@example.com": {"password": "senha1"},
    "user2@example.com": {"password": "senha2"}
}

# Armazenamento temporário de tokens de recuperação
recovery_tokens = {}


class RequestPasswordResetHandler(RequestPasswordResetHandler):
    
    urls = [r"/api/requestPasswordReset/", r"/api/requestPasswordReset"]
    
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        email = data.get('email')

        if email in users:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
            recovery_tokens[email] = token

            # Fazer função de envio de email send_recovery_email(email, token)

            self.write({"message": "Email enviado com sucesso."})
        else:
            self.set_status(404)
            self.write({"error": "Usuário não encontrado."})


class ResetPasswordHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        email = data.get('email')
        new_password = data.get('new_password')

        if email in users:
            users[email]['password'] = new_password
            
            if email in recovery_tokens:
                del recovery_tokens[email]

            self.write({"message": "Senha redefinida com sucesso."})
        else:
            self.set_status(404)
            self.write({"error": "Usuário não encontrado."})


def make_app():
    return tornado.web.Application([
        (r"/api/request-password-reset", RequestPasswordResetHandler),
        (r"/api/reset-password", ResetPasswordHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
