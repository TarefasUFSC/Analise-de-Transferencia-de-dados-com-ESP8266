from ExperimentArguments import ExperimentArguments
from ESPSerial import ESPSerial
import pandas as pd
import numpy as np
class ExperimentWrapper():
    def __init__(self, raw_arguments):
        """Construtor do ExperimentWrapper"""
        self.experiment_arguments = ExperimentArguments(raw_arguments)
        print(self.experiment_arguments)

        self._load_dataframe()
    def _load_dataframe(self):
        self.dataframe = pd.read_csv('data.csv', index_col=False)
        self._size_bytes = self.dataframe['QTD_Bytes'].to_list()
        self._distance_m = self.dataframe['Distancia_m'].to_list()
        self._tempo_ms = self.dataframe['Tempo_ms'].to_list()
        self._walls = self.dataframe['QTD_Paredes'].to_list()
        self._wifi = self.dataframe['INT_WIFI'].to_list()
        self._wifi_same_channel = self.dataframe['INT_WIFI-Mesmo_Canal'].to_list()
        self._wifi_near = self.dataframe['INT_WIFI-Proximo'].to_list()
        self._bluetooth = self.dataframe['INT_BT'].to_list()
        self._bluetooth_near = self.dataframe['INT_BT-Proximo'].to_list()
        self._microwave = self.dataframe['INT_MICROONDAS'].to_list()
        self._microwave_near = self.dataframe['INT_MICROONDAS-Proximo'].to_list()
        self._electromagnetic = self.dataframe['INT_FURADEIRA'].to_list()
        self._electromagnetic_near = self.dataframe['INT_FURADEIRA-Proximo'].to_list()
    
    def _save_dataframe(self):
        self.dataframe = pd.DataFrame({
            'QTD_Bytes': self._size_bytes,
            'Distancia_m': self._distance_m,
            'Tempo_ms': self._tempo_ms,
            'QTD_Paredes': self._walls,
            'INT_WIFI': self._wifi,
            'INT_WIFI-Mesmo_Canal': self._wifi_same_channel,
            'INT_WIFI-Proximo': self._wifi_near,
            'INT_BT': self._bluetooth,
            'INT_BT-Proximo': self._bluetooth_near,
            'INT_MICROONDAS': self._microwave,
            'INT_MICROONDAS-Proximo': self._microwave_near,
            'INT_FURADEIRA': self._electromagnetic,
            'INT_FURADEIRA-Proximo': self._electromagnetic_near
        })
        self.dataframe.to_csv('data.csv', index=False)

    def run_experiment(self):
        """Executa o experimento"""
        esp_serial = ESPSerial(self.experiment_arguments.port)
        experiment_data = esp_serial.run_experiment()

        if(experiment_data is None or experiment_data == {}):
            raise Exception("O experimento não retornou nenhum dado.")
        
        # pega as chaves fo dicionario
        keys = experiment_data.keys()
        for key in keys:
            # cada chave é um size
            self._size_bytes.append(key)
            self._tempo_ms.append(np.array(experiment_data[key]).mean())

            # adiciona os argumentos do experimento
            self._distance_m.append(self.experiment_arguments.distance)
            self._walls.append(self.experiment_arguments.walls)
            self._wifi.append(1 if self.experiment_arguments.wifi != None else 0)
            self._wifi_same_channel.append(self.experiment_arguments.wifi)
            self._wifi_near.append(self.experiment_arguments.wifi_location)
            self._bluetooth.append(1 if self.experiment_arguments.bluetooth != None else 0)
            self._bluetooth_near.append(self.experiment_arguments.bluetooth)
            self._microwave.append(1 if self.experiment_arguments.microwave != None else 0)
            self._microwave_near.append(self.experiment_arguments.microwave)
            self._electromagnetic.append(1 if self.experiment_arguments.electromagnetic != None else 0)
            self._electromagnetic_near.append(self.experiment_arguments.electromagnetic)

        self._save_dataframe()

        return
    
    