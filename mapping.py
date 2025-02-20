from utils import read_json, write_json, csv_to_dict_list

def get_ref_translation(en_translations):
    ref_translation = ""
    for translation in en_translations:
        ref_translation += f' {translation}'
    return ref_translation

def map_translations(dpo_translations, zero_shot_translations):
    translations = []

    for dpo_translation, seg_translations in zip(dpo_translations, zero_shot_translations):
        bo_seg = seg_translations['bo']
        ref_translation = get_ref_translation(seg_translations['en'])
        translations.append({
            'bo': bo_seg,
            'dpo_translation': dpo_translation,
            'ref_translation': ref_translation
        })
    return translations

def get_dpo_translations():
    dpo_tranlsations = []
    dpo_data = csv_to_dict_list('data/gongpa_rabsel/dpo_translations.csv')
    for row in dpo_data:
        dpo_tranlsations.append(row['Target_dpo'])
    return dpo_tranlsations


if __name__ == '__main__':
    # zero_shot_translations = read_json('data/gongpa_rabsel/translations.json')
    # dpo_tranlations = get_dpo_translations()
    # translations = map_translations(dpo_tranlations, zero_shot_translations)
    # write_json('./data/gongpa_rabsel/mapped_translations.json', translations)
    translations = csv_to_dict_list('data/heart_sutra/translations.csv')
    write_json('./data/heart_sutra/mapped_translations.json', translations)