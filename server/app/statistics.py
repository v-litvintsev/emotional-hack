from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel



class Emotion():

    def emotion_message(message:str):
        FastTextSocialNetworkModel.MODEL_PATH = './fasttext-social-network-model.bin'
        tokenizer = RegexTokenizer()
        model = FastTextSocialNetworkModel(tokenizer=tokenizer)

        msg = [message]
        results = model.predict(msg,k =2)
        res = results[0]
        for key, value in res.items():
            return key


