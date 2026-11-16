class Betting:


    def __init__(self, balance):
        self.balance = balance
        self.initial_balance = balance
        self.history = []


    def validate_bet(self, amount):
        if amount <= 0 or amount > self.balance:
            return False
        else:
            return True


    def check_prediction(self, current_rate, next_rate, prediction):
        if prediction not in ('up', 'not_up'):
            raise ValueError('Invalid prediction')

        if prediction == 'up':
            return next_rate > current_rate
        else:
            return next_rate <= current_rate


    def calculate_result(self, amount, is_correct):
        if is_correct:
            return round(amount * 0.1, 2)
        else:
            return -round(amount * 0.1, 2)


    def update_balance(self, result):
        self.balance += result
        self.balance = round(self.balance, 2)
        return self.balance

    
    def add_to_history(self, amount, prediction, current_rate,
                       next_rate, is_correct, result):

        round_data = {
            'amount': amount,
            'prediction': prediction,
            'current_rate': current_rate,
            'next_rate': next_rate,
            'is_correct': is_correct,
            'result': result,
            'balance_after': self.balance
        }

        self.history.append(round_data)
