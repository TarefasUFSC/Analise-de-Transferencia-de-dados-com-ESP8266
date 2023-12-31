
class ExperimentArguments():
    def __init__(self, args):
        """Construtor dos Argumentos do Experimento. Aqui Também é feita a validação dos argumentos"""
        
        self._validate_port(args.port)
        self._validate_distance(args.distance)
        self._validate_walls(args.walls)
        self._validate_wifi(args.wifi, args.wifi_location)
        self._validate_bluetooth(args.bluetooth)
        self._validate_microwave(args.microwave)
        self._validate_cem(args.electromagnetic)
        

    def _validate_port(self,port):
        if(port == None):
            raise Exception("\033[91mA porta serial do ESP não foi informada.\033[0m")
        self.port = port

    def _validate_distance(self,distance):
        if(distance == None):
            raise Exception("\033[91mA distância entre os ESPs não foi informada.\033[0m")
        self.distance = distance
    
    def _validate_walls(self,walls):
        if(int(walls)<0):
            raise Exception("\033[91mA quantidade de paredes deve ser um número inteiro positivo.\033[0m")
        self.walls =  int(walls)

    def _validate_wifi(self,wifi, wifi_location):
        if(wifi != 'SAME' and wifi != 'DIFF' and wifi != ''):
            raise Exception("\033[91mA interferência wifi deve ser SAME ou DIFF.\033[0m")
        if(wifi != ''):
            if(wifi_location != 'CLIENT' and wifi_location != 'SERVER'):
                raise Exception("\033[91mA localização da interferência wifi deve ser CLIENT ou SERVER.\033[0m")
            self.wifi_location = wifi_location
            self.wifi = wifi
        else:
            self.wifi_location = None
            self.wifi = None

    def _validate_bluetooth(self,bluetooth):
        if(bluetooth != 'CLIENT' and bluetooth != 'SERVER' and bluetooth != ''):
            raise Exception("\033[91mA interferência bluetooth deve ser CLIENT ou SERVER.\033[0m")
        self.bluetooth = bluetooth if bluetooth != '' else None
    
    def _validate_microwave(self,microwave):
        if(microwave != 'CLIENT' and microwave != 'SERVER' and microwave != ''):
            raise Exception("\033[91mA interferência com microondas deve ser CLIENT ou SERVER.\033[0m")
        self.microwave = microwave if microwave != '' else None

    def _validate_cem(self,electromagnetic):
        if(electromagnetic != 'CLIENT' and electromagnetic != 'SERVER' and electromagnetic != ''):
            raise Exception("\033[91mA interferência com campo eletromagnético deve ser CLIENT ou SERVER.\033[0m")
        self.electromagnetic = electromagnetic if electromagnetic != '' else None

    def __str__(self):
        description_string = f"O experimento sera realizado conectado na porta {self.port} com os seguintes argumentos:\nDistancia de {self.distance} metros entre os ESPs\n{self.walls} paredes entre os ESPs\n"
        if(self.wifi != None):
            description_string += f"Interferência wifi: {self.wifi} no {self.wifi_location}\n"
        if(self.bluetooth != None):
            description_string += f"Interferência bluetooth: {self.bluetooth}\n"
        if(self.microwave != None):
            description_string += f"Interferência com microondas: {self.microwave}\n"
        if(self.electromagnetic != None):
            description_string += f"Interferência com campo eletromagnético: {self.electromagnetic}\n"
        return description_string