from django import template

register = template.Library()

words_to_change = ['fuck', 'bitch', 'arsehole', 'balls', 'bollocks', 'bullshit', 'feck', 'shit']
signs = ['.', ',', '!', '?', ':']
signs_2 = ['\'', '"']


@register.filter()
def censor(value):
    result = []
    if value and isinstance(value, str):
        for word in value.split():
            if word[-1] in signs:
                result.append(word[0] + '*' * (len(word) - 2) + word[-1]) if word[:-1].lower() in words_to_change\
                    else result.append(word)
            elif word[0] in signs_2:
                result.append(word[0] + word[1] + ('*' * (len(word) - 3)) + word[-1]) if word[1:-1].lower() in words_to_change\
                    else result.append(word)
            else:
                result.append(word[0] + '*' * (len(word) - 1)) if word.lower() in words_to_change else result.append(word)
        return ' '.join(result)
    else:
        raise TypeError


@register.filter()
def minus(value, arg):
    return value - int(arg)
