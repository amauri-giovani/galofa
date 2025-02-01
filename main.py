import os
from itertools import combinations
from pprint import pprint
from random import sample
import pandas as pd
from results_download import results_download


class Galofa:
    def __init__(self):
        self.todas_combinacoes_possiveis = list(combinations(range(1, 26), 15))
        self.file_reader = pd.read_excel(self.get_filename())
        self.frequencias_numeros_sorteados = self.get_frequency_in_draws()
        self.sorteios_realizados = self.create_dataframe_draws()
        self.qtde_sorteios_repetidos = self.sorteios_realizados.sorteados.duplicated().sum()
        self.lista_numeros_sorteados = self.sorteios_realizados.sorteados.values.tolist()
        self.combinacoes_nao_sorteadas = set(self.todas_combinacoes_possiveis) - set(self.lista_numeros_sorteados)

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

    def generate_bets(self, numbers: int = 15, bets_quantity: int = 1) -> list:
        if numbers == 15:
            return sample(list(self.combinacoes_nao_sorteadas), bets_quantity)
        return sample(list(combinations(range(1, 26), numbers)), bets_quantity)

    def check_draw_result_by_result(self, bets: list, result: set = None):
        if not result:
            print(self.sorteios_realizados.iloc[-1])
            result = self.lista_numeros_sorteados[-1]
        response = []
        for bet in bets:
            response.append({str(bet): f'{len(set(bet) & set(result))} acertos'})
        print('\nResultado: result\n')
        print('Quantidade de acertos em cada aposta\n')
        return response

    def check_draw_result_by_contest(self, bets: list, contest_number: int = None):
        if not contest_number:
            print(self.sorteios_realizados.iloc[-1])
            result = self.lista_numeros_sorteados[-1]
        else:
            contest = self.sorteios_realizados[self.sorteios_realizados['concurso'] == contest_number]
            contest_dict = contest.to_dict(orient='records')[0]
            print(f'\n{'='*90}\nConcurso: {contest_dict["concurso"]}\nData do Sorteio: {contest_dict["data"]}\n'
                  f'Números sorteados: {' - '.join(map(str, contest_dict["sorteados"]))}\n{'='*90}\n')
            result = contest['sorteados'].tolist()[0]
        response = []
        for bet in bets:
            response.append({str(bet): f'{len(set(bet) & set(result))} acertos'})
        print('Quantidade de acertos em cada aposta\n')
        return response


pd.set_option("display.max_colwidth", None)
galofa = Galofa()
# response = galofa.check_draw_result_by_contest([
#     {1, 2, 4, 8, 9, 11, 12, 13, 16, 18, 20, 21, 22, 23, 25},
#     {1, 4, 6, 8, 10, 12, 13, 15, 16, 18, 20, 21, 22, 23, 25},
#     {1, 2, 5, 6, 8, 10, 11, 12, 15, 16, 17, 20, 23, 24, 25},
#     {2, 5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 21, 22, 23},
#     {1, 3, 4, 5, 7, 8, 14, 16, 17, 18, 20, 21, 22, 23, 25},
#     {1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 20, 23, 25},
#     {1, 2, 4, 5, 6, 8, 10, 13, 17, 18, 19, 21, 23, 24, 25},
#     {1, 4, 5, 7, 10, 13, 14, 15, 16, 18, 20, 21, 22, 23, 25},
#     {1, 2, 3, 5, 10, 11, 14, 15, 17, 19, 20, 22, 23, 24, 25},
#     {1, 2, 5, 6, 7, 8, 9, 15, 17, 18, 21, 22, 23, 24, 25}
# ], contest_number=3307)
# pprint(response)
print()