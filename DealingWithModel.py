from emotion_recognition import EmotionRecognizer
from sklearn.neural_network import MLPClassifier

def test_9_emotions():

    my_model = MLPClassifier()

    rec = EmotionRecognizer(model=my_model, emotions=["neutral","calm","happy","sad","angry","fear","disgust","ps", "boredom"], balance=True, verbose=0)
    # train the model
    rec.train()

    rec.determine_best_model()

    return rec
