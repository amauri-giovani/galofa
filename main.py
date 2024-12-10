from itertools import combinations
from random import choices, choice
import pandas as pd


class Galofa:
    def __init__(self, file_path):
        self.todas_combinacoes_possiveis = combinations(range(1, 26), 15)
        self.file_reader = pd.read_excel(file_path)
        self.frequencias_numeros_sorteados = self.get_frequency_in_draws()
        self.sorteios_realizados = self.create_dataframe_draws()
        self.qtde_sorteios_repetidos = self.sorteios_realizados.sorteados.duplicated().sum()
        self.lista_numeros_sorteados = self.sorteios_realizados.sorteados.values.tolist()

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
file_path = "files/Lotofácil.xlsx"
galofa = Galofa(file_path)
print()