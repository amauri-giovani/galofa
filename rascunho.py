from itertools import combinations
from random import choices, choice
import pandas as pd


pd.set_option("display.max_colwidth", None)


class Galofa:
    def __init__(self, file_path):
        self.all_combinations = combinations(range(1, 26), 15)
        self.file_reader = pd.read_excel(file_path)
        # self.df_only_draws_numbers = self.file_reader.loc[1:, 'Bola1':'Bola15']
        self.draws = self.create_dataframe_draws()
        self.df = None
        # self.draws_numbers = self.draws["sorteados"]
        self.number_if_repeated_draws = self.draws.sorteados.duplicated().sum()
        self.checks_for_duplicate_results = self.draws.sorteados.duplicated().value_counts()
        self.list_of_draws_numbers = self.draws.sorteados.values.tolist()
        self.frequencies = self.get_frequency_in_draws()
        self.best_betting_suggestions = None
        self.best_next_undrawn_bets = None
        self.list_combinations = []

    def create_dataframe_draws(self):
        self.draws = self.file_reader.loc[:, "Concurso":"Data Sorteio"]
        self.draws.rename(columns={"Concurso": "concurso", "Data Sorteio": "data"}, inplace=True)
        self.draws["sorteados"] = self.file_reader.loc[:, "Bola1":"Bola15"].values.tolist()
        self.draws["sorteados"] = self.draws["sorteados"].apply(lambda x: tuple(x))
        return self.draws

    def get_frequency_in_draws(self):
        frequencies = []
        df_only_draws_numbers = self.file_reader.loc[1:, 'Bola1':'Bola15']
        for ball_number in range(1, 16):
            frequencies.append(df_only_draws_numbers[f"Bola{ball_number}"].value_counts().to_dict())
        self.frequencies = pd.DataFrame(frequencies).sum().sort_values(ascending=False)
        return self.frequencies

    def most_drawn_numbers(self, quantity=15):
        return tuple(self.frequencies.head(quantity).index.sort_values())

    def check_the_list_of_previous_draws(self):
        return self.most_drawn_numbers() in self.list_of_draws_numbers

    def combines_most_drawn_numbers(self, quantity=16):
        """
        combinations with the sixteen numbers that were most drawn
        :return:
        """
        self.list_combinations = list(combinations(self.most_drawn_numbers(quantity), 15))
        self.best_betting_suggestions = self.list_combinations
        self.check_combines_most_drawn_numbers()

    def check_combines_most_drawn_numbers(self):
        # Verifica se alguma aposta gerada já foi sorteada anteriormente
        suggestions = []
        for suggestion in self.best_betting_suggestions:
            if suggestion not in galofa.list_of_draws_numbers:
                suggestions.append(suggestion)
        self.best_next_undrawn_bets = suggestions

    @property
    def total_combinations(self):
        return f"Total of {len(self.list_combinations)} combinations"

    def choose_bets(self, number_of_bets=1):
        return choices(self.all_combinations, k=number_of_bets)

    def randomly_choose_undrawn_bets(self, number_of_bets=1):
        """
        check if the bet has already been drawn previously
        :return:
        """
        bets = []
        while len(bets) <= number_of_bets:
            bet = choice(self.all_combinations)
            if bet not in self.list_of_draws_numbers:
                bets.append(bet)
        return bets

    def check_draw_result(self, result):
        """
        Passando o resultado do sorteio, verifica se alguma das melhores apostas ganharia
        :param result:
        :return:
        """
        result = set(result)
        list_aux = []
        for bet in self.best_next_undrawn_bets:
            count = 0
            for number in bet:
                if number in result:
                    count += 1
            list_aux.append(f"{bet} ==> {count} hits")
        return list_aux

    # def check_all_draws_with_best_combinations(self):
    #     # list_aux = []
    #     with open("all_draws_with_best_combinations.docx", "w") as docx_file:
    #         for best_combination in self.best_next_undrawn_bets:
    #             list_aux = []
    #             for each_combination in self.all_combinations[:30]:
    #                 total = len(best_combination) - len(set(best_combination) - set(each_combination))
    #                 list_aux.append(f"{each_combination} ==> {total} hits")
    #             docx_file.write(f"{str(list_aux)}\n\n")
    #
    #     return list_aux

    def check_all_draws_with_best_combinations(self):
        colunas = ["aposta", "concurso", "sorteados", "acertos"]
        df = pd.DataFrame(columns=colunas)
        for best_combination in self.best_next_undrawn_bets:
            for each_combination in self.draws.head(30).itertuples():
                numbers = each_combination.sorteados
                total = len(best_combination) - len(set(best_combination) - set(numbers))
                # list_aux.append(f"{each_combination} ==> {total} hits")
                df_aux = pd.DataFrame(
                    {
                        "aposta": [best_combination],
                        "concurso": each_combination.concurso,
                        "sorteados": [each_combination.sorteados],
                        "acertos": total
                    }
                )
                df = pd.concat([df, df_aux], ignore_index=True)
        self.df = df

    """
    Verificar quantos pontos faria em todos os jogos com as melhores apostas
    """


file_path = "files/Lotofácil.xlsx"
galofa = Galofa(file_path)
galofa.get_frequency_in_draws()
galofa.check_the_list_of_previous_draws()
galofa.combines_most_drawn_numbers()
galofa.check_combines_most_drawn_numbers()
galofa.check_all_draws_with_best_combinations()

# resultado = (1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 14, 16, 17, 24, 25)
# resultado = (2, 4, 6, 8, 9, 10, 11, 13, 15, 16, 18, 19, 20, 21, 22)
# resultado = (1, 2, 5, 8, 9, 10, 11, 13, 14, 16, 18, 19, 22, 23, 25)
