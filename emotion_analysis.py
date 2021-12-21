##############################################################################
# Developed by: Shobhit Agarwal
# Algorithm:
# 1.) We are using text2emotion to find textual emotions from text(sentences, words etc.)
# 2.) If the emotion return value is less than 0.3 then we assume it to Neutral.
##############################################################################

# Import packages
import text2emotion as t2e

def extract_emotion(text):

    emotion_dict = t2e.get_emotion(text)
    emotion = max(emotion_dict, key=emotion_dict.get)
    all_values = emotion_dict.values()
    max_value = max(all_values)
    if max_value < 0.3:
        return 'Neutral'
    return emotion

if __name__ == '__main__':
    print(extract_emotion('This is so disgraceful'))
