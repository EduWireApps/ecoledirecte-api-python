from requests import post, Session
import requests
import json
from datetime import date


class Client:

    def __init__(self, ident, password, keepSession=True):
        self.__idents = [ident,password]
        self.BASE = "https://api.ecoledirecte.com/v3/"
        self.__BASEHEADER= {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        self.LOGINPAYLOAD = 'data={"uuid": "","identifiant": "' + ident + '","motdepasse":"' + password + '","isReLogin": false}'
        self.__PARAMS = {"verbe": "get", "v":"4.26.3"}

        if keepSession:
            self.session = Session()
            self.raw_data = self.session.post(self.BASE + "/login.awp?v=4.26.3", data=self.LOGINPAYLOAD, headers=self.__BASEHEADER).json()
        else:
            self.session = None
            self.raw_data = post(self.BASE + "/login.awp?v=4.26.3", data=self.LOGINPAYLOAD,headers=self.__BASEHEADER).json()

        if self.raw_data['message']:
            raise ConnectionRefusedError(f"[{self.raw_data['code']}] {self.raw_data['message']}")
        self.data = self.raw_data['data']
        self.token = self.raw_data['token']
        self.user = self.data['accounts'][0]
        self.id = self.user['id']
        self.type = self.user['typeCompte']

        self.__HEADERS = {"x-token":self.token,
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

    # Raw_Request permet lui d'avoir une base mais vous devez faire toute la route, (pour les cas particuliers de l'API)

    def raw_request(self, route: str, headers=None, params=None, data=None) -> requests.Response:
        url = self.BASE + route
        config = {"headers":self.__HEADERS,"params":self.__PARAMS}
        if headers:
            config["headers"] = headers
        if params:
            config["params"] = params

        if self.session:
            r = self.session.post(url=url, headers=config.get("headers"),
                                  params=config.get("params"),
                                  data=data)
        else:
            r = post(url=url, headers=config.get("headers"),
                     params=config.get("params"),
                     data=data)

        return r


class Eleve(Client):

    def __init__(self, ident, password, keepSession = True):
        super(Eleve, self).__init__(ident=ident,password=password, keepSession=keepSession)

        if self.type != 'E':
            raise ReferenceError("Ce compte n'est pas un compte élève")

        self.prenom = self.user['prenom']
        self.nom = self.user['nom']
        self.etablissement = self.user['nomEtablissement']
        self.derniereConnec = self.user['lastConnexion']
        self.modules = self.user['modules']
        self.parametres = self.user['parametresIndividuels']

        self.sexe = self.user['profile']['sexe']
        self.telPortable = self.user['profile']['telPortable']
        self.photo = self.user['profile']['photo']
        self.classe = self.user['profile']['classe']

    def getRawNotes(self, anneeSco:int=None) -> dict:
        route = "eleves/" + str(self.id) + "/notes.awp"
        payload = 'data={"anneeScolaire": ""}'
        if anneeSco:
            payload = 'data={"anneeScolaire": "' + anneeSco + '"}'
        r = self.raw_request(route,data=payload)
        return r.json()


    def getRawEmploiDuTemps(self, dateDebut:date = None, dateFin:date= None) -> dict:
        if dateDebut and not dateFin:
            dateDebut = dateDebut.isoformat()
            dateFin = dateDebut
        elif not dateDebut and dateFin:
            dateDebut = date.today().isoformat()
            dateFin = dateFin.isoformat()
        elif not dateDebut and not dateFin:
            dateDebut = date.today().isoformat()
            dateFin = date.today().isoformat()
        else:
            dateDebut = dateDebut.isoformat()
            dateFin = dateFin.isoformat()
        route = "E/" + str(self.id) + "/emploidutemps.awp"
        payload = 'data={"dateDebut": "' + dateDebut + '","dateFin":"' + dateFin + '","avecTrous": false}'
        return self.raw_request(route, data=payload).json()

    def getEmploiDuTemps(self, dateDebut:date = None, dateFin:date = None) -> list:
        edt = self.getRawEmploiDuTemps(dateDebut,dateFin)
        self.token = edt['token']
        return edt['data']


test = Eleve("PETRUCCI","EcoleDirecte20!")
print(test.getRawEmploiDuTemps(date(2023,2,20)))



