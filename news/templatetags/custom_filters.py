from django import template

register = template.Library()


@register.filter()
def censor(text):
    bad_words = ('badword', )

    if not isinstance(text, str):
        raise TypeError(f"unresolved type '{type(text)}' expected  type 'str'")

    for word in text.split():
        if word.lower() in bad_words:
            text = text.replace(word, f"{word[0]}{'*' * (len(word) - 1)}")
    return text
