from llm import get_claude_response
from utils import parse_tag_response, read_json, write_json

def get_improved_translation(source_text, draft_translation_1, draft_translation_2):
    prompt = f"""
Here is a Tibetan text with 2 draft translations.  
Tibetan text: {source_text}

Draft 1: {draft_translation_2}

Draft 2: {draft_translation_1}
1. Extract all named entities including names of spiritual states from draft 1.

2. Generate your own translation using the named entities but with your own text. 

3. Criticise Draft 1 and Draft 2 by identifying all translation errors from the following list. Ignore potential errors related with the above named entities: 
- Instances of omissions, 
- Instances of additions,  
- Instances of mistranslations,  
- Instances of untranslated words, 
- Instances of grammar mistakes,  
- Instances of punctuation issues, 
- Instances of inconsistent terminology,  
- Instances of inappropriate terminology, 
- Instances of unidiomatic language,  
- Instances of inconsistent style, 
- Instances of technical accuracy errors, 
- Instances of cultural accuracy errors.

4. Translate the text using all the extracted named entities and with all the errors fixed.
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
                },

            ]
    translation_with_critic = get_claude_response(message)
    final_prompt = f"""
Based on the above criticism and improved translation, generate the following: 
1. A plain English "easy-to-read" version that preserves people and text names. Put the final translation in <plain> tags.
2. A complete word-by-word translation of the ENTIRE Tibetan text, with no omissions or summarising; showing each Tibetan word in unicode followed by its English meaning in square brackets and put the result in <wbw> tags.
3. A literal translation combining the word by word translation with the meaning of the plain English translation, put the translation in <lt> tags.
"""
    message.append(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": translation_with_critic
                }
            ]
        }
    )
    message.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": final_prompt
                }
            ]
        }
    )

    improved_translation = get_claude_response(message)
    plain_translation_tag = "<plain>(.*?)</plain>"
    plain_translation = parse_tag_response(plain_translation_tag, improved_translation)
    word_to_word_translation_tag = "<wbw>(.*?)</wbw>"
    word_to_word_translation = parse_tag_response(word_to_word_translation_tag, improved_translation)
    literal_translation_tag = "<lt>(.*?)</lt>"
    literal_translation = parse_tag_response(literal_translation_tag, improved_translation)
    ai_tranlsations = {
        'traslation_with_critic': translation_with_critic,
        'easy_translation': plain_translation,
        'word_by_word_translation': word_to_word_translation,
        'literal_translation': literal_translation,
    }

    return ai_tranlsations

def get_ref_base_ai_translation(tranlation_data):
    reference_base_ai_translation = []
    for seg_walker, translation in enumerate(tranlation_data, 1):
        source_text = translation['bo']
        ai_translation = translation['dpo_translation']
        human_translation = translation['ref_translation']
        ai_translations = get_improved_translation(source_text, ai_translation, human_translation)
        reference_base_ai_translation.append({
            'bo': source_text,
            'dpo_translation': ai_translation,
            'ref_translation': human_translation,
            'translation_with_critic': ai_translations.get('traslation_with_critic', ''),
            'easy_translation': ai_translations.get('easy_translation', ''),
            'word_by_word_translation': ai_translations.get('word_by_word_translation', ''),
            'literal_translation': ai_translations.get('literal_translation', ''),
        })
        print(f"Segment {seg_walker} done.")
    return reference_base_ai_translation


if __name__ == '__main__':
    translation_data = read_json('data/gongpa_rabsel/mapped_translations.json')
    reference_base_ai_translation = get_ref_base_ai_translation(translation_data)
    write_json('data/gongpa_rabsel/En_translation.json', reference_base_ai_translation)
    # translation_data = read_json('data/heart_sutra/mapped_translations.json')
    # reference_base_ai_translation = get_ref_base_ai_translation(translation_data)
    # write_json('data/heart_sutra/final_translation.json', reference_base_ai_translation)
