import random as r
import re
import string

class Roll:
    def __init__(self, current=None, maximum=20):
        if current == None:
            self.current = r.randint(1, maximum)
        else:
            self.current = current
        self.maximum = maximum

    def __str__(self):
        return f'roll: {self.current}/{self.maximum}'

    def to_tuple(self):
        return (self.current, self.maximum)

    def reroll(self):
        self.current = r.randint(1, self.maximum)

def single_roll(dice:int) -> Roll:
    return Roll(maximum=dice)

def list_roll(dice:int, n:int):
    return [Roll(maximum=dice) for _ in range(n)]

def up_list_roll(dice:int, n:int, top:int=1):
    if top > n:
        top = n
    roll_list = list_roll(dice=dice, n=n)
    maximum = sorted(roll_list, key = lambda x: x.current, reverse=True)[:top]
    return list(maximum), roll_list

def down_list_roll(dice:int, n:int, top:int=1):
    if top > n:
        top = n
    roll_list = list_roll(dice=dice, n=n)
    minimum = sorted(roll_list, key = lambda x: x.current)[:top]
    return minimum, roll_list

def parse_roll_command(message_text: str) -> str:
    """ parses a roll command text
        calls the requred functions
        returns string with rolls result"""

    dice = int(re.search(r'[dD](\d+)', message_text).group(1))

    if not message_text[0].isdigit():
        if not any(c in message_text for c in '+-*/'):
            return str(single_roll(dice))
        else:
            sign = re.search(r'[+\-*/]', message_text).group()
            _, added = message_text.split(sign)
            added = int(added.strip())
            roll = single_roll(dice).to_tuple()
            match sign:
                case '+':
                    return f'roll: {roll[0] + added}/{roll[1]+added} ({roll[0]}+{added})'
                case '-':
                    if added > roll[1]:
                        return f'error: {added} больше, чем {roll[1]})'
                    if added > roll[0]:
                        curr = 0
                    else:
                        curr = roll[0]- added
                    return f'roll: {curr}/{roll[1]-added} ({roll[0]}-{added})'
                case '*':
                    return f'roll: {roll[0] * added}/{roll[1]*added} ({roll[0]}*{added})'
                case '/':
                    return f'roll: {round(roll[0] / added)}/{round(roll[1]/added)} ({roll[0]}/{added})'
                case _:
                    return 'bad request'
    else:
        num = int(re.match(r'\d+', message_text).group())
        if not re.search(r'[hlHL]', message_text):
            rolls = list_roll(dice=dice, n=num)
            if not re.search(r'[+\-*/]', message_text):
                return 'roll: [' + ', '.join(f'{r.current}' for r in rolls) + \
                        ']=' + str(sum(r.current for r in rolls))
            else:
                sign = re.search(r'[+\-*/]', message_text).group()
                added = int(re.search(r'[+\-*/](\d+)', message_text).group(1))
                match sign:
                    case '+':
                        rollsum = sum(r.current for r in rolls)
                        return 'roll: [' + ', '.join(f'{r.current}' for r in rolls) + \
                                ']=<b>' + str(rollsum + added) + f'</b> ({rollsum}+{added})'
                    case '-':
                        rollsum = sum(r.current for r in rolls)
                        result = rollsum -added
                        if rollsum < added:
                            result=0
                        return 'roll: [' + ', '.join(f'{r.current}' for r in rolls) + \
                                ']=<b>' + str(result) + f'</b> ({rollsum}-{added})'
                    case '*':
                        rollsum = sum(r.current for r in rolls)
                        return 'roll: [' + ', '.join(f'{r.current}' for r in rolls) + \
                                ']=<b>' + str(rollsum * added) + f'</b> ({rollsum}*{added})'
                    case '/':
                        rollsum = sum(r.current for r in rolls)
                        return 'roll: [' + ', '.join(f'{r.current}' for r in rolls) + \
                                ']=<b>' + str(round(rollsum / added)) + f'</b> ({rollsum}/{added})'

        else:
            top = int(re.search(r'[hHlL](\d+)', message_text).group(1))
            if re.search(r'[hH]', message_text):
                maximums, rolls = up_list_roll(dice, num, top)
                if not any(c in message_text for c in '+-*/'):
                    return 'roll: [' + ','.join(str(r.current) for r in maximums) + ']' + f'=<b>{sum(r.current for r in maximums)}</b>' + \
                            ' (' + ','.join(str(r.current) for r  in rolls) + ')'
                            

            elif re.search(r'[lL]', message_text):
                minimums, rolls = down_list_roll(dice, num, top)
                if not any(c in message_text for c in '+-*/'):
                    return 'roll: [' + ','.join(str(r.current) for r in minimums) + ']' + f'=<b>{sum(r.current for r in minimums)}</b>' + \
                            ' (' + ','.join(str(r.current) for r  in rolls) + ')'
