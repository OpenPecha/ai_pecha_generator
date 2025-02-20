from llm import get_claude_response
from utils import read_json, write_json, parse_tag_response

def get_russian_translation(source_text, en_translation):
    prompt = f"""
Вы профессионал в тибетском буддизме и вы прекрасно владеете тибетским, английским и русским. Здесь предоставлен текст на тибетском языке и его перевод на английский. Вот тибетский текст с его английским переводом и глоссарием.

Тибетский текст: {source_text}

Английский перевод: {en_translation}

Для перевода этого текста на русский язык выполни следующие шаги:

1. Проанализируй тибетский текст и его английский перевод.

2. Составь черновой перевод на русский язык.

3. Проанализируй черновой перевод, выявляя ошибки из следующего списка:

• Пропуски,
• Добавления,
• Ошибки в передаче смысла,
• Непереведённые слова,
• Грамматические ошибки,
• Ошибки пунктуации,
• Несогласованность терминологии,
• Неправильное использование терминов,
• Неестественные для русского языка формулировки,
• Несогласованность стиля,
• Ошибки в передаче специализированных понятий,
•  Ошибки, искажающие культурный контекст.

4. Переведи текст на русский язык, исправив все ошибки. Помести итоговый перевод в <t> теги.
"""
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
    translation_responses = get_claude_response(message)
    ru_translation = "<t>(.*?)</t>"
    russian_translation = parse_tag_response(ru_translation, translation_responses)
    return russian_translation


def get_russian_translations(translation_data):
    russian_translations = []
    for seg_walker, translation in enumerate(translation_data, 1):
        source_text = translation['bo']
        en_translation = translation['ref_translation']
        russian_translation = get_russian_translation(source_text, en_translation)
        russian_translations.append({
            'bo': source_text,
            'en_translation': en_translation,
            'ru_translation': russian_translation
        })
        print(f"Segment {seg_walker} done.")
    return russian_translations

if __name__ == "__main__":
    translation_data = read_json('data/gongpa_rabsel/src_and_ref.json')
    russian_translations = get_russian_translations(translation_data)
    write_json('data/gongpa_rabsel/ru_translation.json', russian_translations)