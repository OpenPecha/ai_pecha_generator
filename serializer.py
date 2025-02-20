from pathlib import Path

from utils import read_json, write_json

def preprocess_translations(translation):
    translation = translation.strip()
    translation = translation.replace("\n", "$")
    return translation


def serialize_translations(translations):
    # serialized_translations = {
    #     'bo': '',
    #     'melong_translation': '',
    #     'easy_translation': '',
    #     'word_by_word_translation': '',
    #     'literal_translation': '',
    # }
    serialized_translations = {
        'bo': '',
        'ru_translation': '',
    }
    for seg_walker, translation in enumerate(translations, 1):
        source_text = preprocess_translations(translation['bo'])
        ru_translation = preprocess_translations(translation.get('ru_translation', ''))
        serialized_translations['bo'] += f'{source_text}\n'
        serialized_translations['ru_translation'] += f'{ru_translation}\n'
    return serialized_translations

if __name__ == "__main__":
    translations = read_json('data/gongpa_rabsel/ru_translation.json')
    serialized_translations = serialize_translations(translations)
    serialized_translation_dir = Path('./data/gongpa_rabsel/serialized_translations')
    serialized_translation_dir.mkdir(parents=True, exist_ok=True)
    for translation_type, translation in serialized_translations.items():
        (serialized_translation_dir / f'{translation_type}.txt').write_text(translation, encoding='utf-8')
        