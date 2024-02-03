import requests
from kivy.app import App 

class MyFirebase():
    API_KEY = "AIzaSyCdU0vkGss9PYj8fCUtEq2HWwnfO7y5ESI"
    def criar_conta(self, email, senha, telefone):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        info = {"email": email, "password": senha, "returnSecureToken": True}
        print(email, senha)
        requisicao = requests.post(link, data = info)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        
        if requisicao.ok:
            print("Usuario Criado.")
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]


            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            
            link = f"https://app-psicologia-66b64-default-rtdb.firebaseio.com/{local_id}.json"
            info_usuario = f'{{"minhas_sessoes": "", "email": "{email}", "telefone": "{telefone}"}}'
            requisicao_usuario = requests.patch(link, data = info_usuario)
            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela("menu")

        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            # mensagem_erro = mensagem_erro.replace("MISSING_PASSWORD", "Senha inválida")
            # aqui coloca a traducao
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text=mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1,0,0,1)
        print(requisicao_dic)
    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info = {"email": email, "password": senha, "returnSecureToken": True}
        print(email, senha)
        requisicao = requests.post(link, data = info)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        
        if requisicao.ok:
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]


            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            meu_aplicativo.carregar_infos_usuario()
            if email == "admin@gmail.com":
                meu_aplicativo.mudar_tela("menuadmin")
            else:
                meu_aplicativo.mudar_tela("menu")

        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            # mensagem_erro = mensagem_erro.replace("MISSING_PASSWORD", "Senha inválida")
            # aqui coloca a traducao
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text=mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1,0,0,1)
        pass
    
    def trocar_token(self, refresh_token):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        info = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        requisicao = requests.post(link, data = info)
        requisicao_dic = requisicao.json()
        local_id = requisicao_dic["user_id"]
        id_token = requisicao_dic["id_token"]
        return local_id, id_token