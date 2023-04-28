from emotion_recognition import EmotionRecognizer
from parameters import classifier_model, emotions, dataset, hyper_parameter, verbose, balance


def test_9_emotions():

    rec = EmotionRecognizer(model=classifier_model,
                            emotions=emotions,
                            dataset=dataset,
                            tess_ravdess=dataset.get("tess_ravdess", True),
                            emodb=dataset.get("emodb", True),
                            custom_db=dataset.get("custom_db", True),
                            # , balance=balance
                            verbose=verbose
                            )

    rec.determine_best_model()

    return rec
