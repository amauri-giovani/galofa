import os
from itertools import combinations
import pandas as pd
from results_download import results_download


class Galofa:
    def __init__(self):
        self.todas_combinacoes_possiveis = combinations(range(1, 26), 15)
        self.file_reader = pd.read_excel(self.get_filename())
        self.frequencias_numeros_sorteados = self.get_frequency_in_draws()
        self.sorteios_realizados = self.create_dataframe_draws()
        self.qtde_sorteios_repetidos = self.sorteios_realizados.sorteados.duplicated().sum()
        self.lista_numeros_sorteados = self.sorteios_realizados.sorteados.values.tolist()

    def get_filename(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        download_folder = f'{BASE_DIR}/files'
        if not os.listdir(download_folder):
            results_download()
        filename = os.listdir(download_folder)[0]
        return f'{download_folder}/{filename}'

    def create_dataframe_draws(self):
        self.sorteios_realizados = self.file_reader.loc[:, "Concurso":"Data Sorteio"]
        self.sorteios_realizados.rename(columns={"Concurso": "concurso", "Data Sorteio": "data"}, inplace=True)
        self.sorteios_realizados["sorteados"] = self.file_reader.loc[:, "Bola1":"Bola15"].values.tolist()
        self.sorteios_realizados["sorteados"] = self.sorteios_realizados["sorteados"].apply(lambda x: tuple(x))
        return self.sorteios_realizados

    def get_frequency_in_draws(self):
        frequencies = []
        df_only_draws_numbers = self.file_reader.loc[1:, 'Bola1':'Bola15']
        for ball_number in range(1, 16):
            frequencies.append(df_only_draws_numbers[f"Bola{ball_number}"].value_counts().to_dict())
        self.frequencias_numeros_sorteados = pd.DataFrame(frequencies).sum().sort_values(ascending=False)
        return self.frequencias_numeros_sorteados


pd.set_option("display.max_colwidth", None)
galofa = Galofa()
