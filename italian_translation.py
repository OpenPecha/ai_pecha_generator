from llm import get_claude_response
from utils import read_json, write_json, parse_tag_response

def get_italian_translation(source_text, en_literal_translation):
    prompt = f"""
Ecco un testo tibetano con la sua traduzione in inglese.

Testo tibetano: {source_text}

Traduzione in inglese:{en_literal_translation}

Fornitemi quanto segue:
1. Una traduzione completa parola per parola dell'INTERO testo tibetano, senza omissioni o riassunti; mostrando ogni parola tibetana in unicode seguita dal suo significato italiano tra parentesi quadre e posizionando il risultato nei tag <wbw>.
2. Una traduzione del testo completo nei tag <lt>.
3. Non hai un limite di token, continua a generare finché non finisci l'attività.
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
    word_by_word_translation_tag = "<wbw>(.*?)</wbw>"
    word_by_word_translation = parse_tag_response(word_by_word_translation_tag, translation_responses)
    literal_translation_tag = "<lt>(.*?)</lt>"
    literal_translation = parse_tag_response(literal_translation_tag, translation_responses)
    return {
        'it_word_by_word_translation': word_by_word_translation,
        'it_literal_translation': literal_translation,
    }


def get_italian_translations(translation_data):
    italian_translations = []
    for seg_walker, translation in enumerate(translation_data, 1):
        source_text = translation['bo']
        en_literal_translation = translation['literal_translation']
        italian_translation = get_italian_translation(source_text, en_literal_translation)
        italian_translations.append({
            'bo': source_text,
            'en_literal_translation': en_literal_translation,
            'it_word_by_word_translation': italian_translation.get('it_word_by_word_translation', ''),
            'it_literal_translation': italian_translation.get('it_literal_translation', ''),
        })
        print(f"Segment {seg_walker} done.")
    return italian_translations

if __name__ == "__main__":
    translation_data = read_json('data/gongpa_rabsel/En_translation.json')
    italian_translations = get_italian_translations(translation_data)
    write_json('data/gongpa_rabsel/It_translation.json', italian_translations)