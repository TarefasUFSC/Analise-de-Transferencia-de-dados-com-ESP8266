
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
            raise Exception("A porta serial do ESP não foi informada.")
        self.port = port

    def _validate_distance(self,distance):
        if(distance == None):
            raise Exception("A distância entre os ESPs não foi informada.")
        self.distance = distance
    
    def _validate_walls(self,walls):
        if(int(walls)<0):
            raise Exception("A quantidade de paredes deve ser um número inteiro positivo.")
        self.walls =  int(walls)

    def _validate_wifi(self,wifi, wifi_location):
        if(wifi != 'SAME' and wifi != 'DIFF' and wifi != ''):
            raise Exception("A interferência wifi deve ser SAME ou DIFF.")
        if(wifi != ''):
            if(wifi_location != 'CLIENT' and wifi_location != 'SERVER'):
                raise Exception("A localização da interferência wifi deve ser CLIENT ou SERVER.")
            self.wifi_location = wifi_location
            self.wifi = wifi
        else:
            self.wifi_location = None
            self.wifi = None

    def _validate_bluetooth(self,bluetooth):
        if(bluetooth != 'SAME' and bluetooth != 'DIFF' and bluetooth != ''):
            raise Exception("A interferência bluetooth deve ser SAME ou DIFF.")
        self.bluetooth = bluetooth if bluetooth != '' else None
    
    def _validate_microwave(self,microwave):
        if(microwave != 'SAME' and microwave != 'DIFF' and microwave != ''):
            raise Exception("A interferência com microondas deve ser SAME ou DIFF.")
        self.microwave = microwave if microwave != '' else None

    def _validate_cem(self,electromagnetic):
        if(electromagnetic != 'SAME' and electromagnetic != 'DIFF' and electromagnetic != ''):
            raise Exception("A interferência com campo eletromagnético deve ser SAME ou DIFF.")
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