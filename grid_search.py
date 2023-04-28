"""
A script to grid search all parameters provided in parameters.py
including both classifiers and regressors.
Note that the execution of this script may take hours to search the 
best possible model parameters for various algorithms, feel free
to edit parameters.py on your need ( e.g remove some parameters for 
faster search )
"""

import pickle

from emotion_recognition import EmotionRecognizer
# from sklearn.neural_network import MLPClassifier
from parameters import classifier_model, emotions, dataset, hyper_parameter

best_estimators = []


rec = EmotionRecognizer(classifier_model, emotions=emotions,
                        tess_ravdess=dataset.get("tess_ravdess", True),
                        emodb=dataset.get("emodb", True),
                        custom_db=dataset.get("custom_db", True),)
rec.load_data()
best_estimator, best_params, cv_best_score = rec.grid_search(
    params=hyper_parameter)

best_estimators.append((best_estimator, best_params, cv_best_score))
print(f"{emotions} {best_estimator.__class__.__name__} achieved {cv_best_score:.3f} cross validation accuracy score!")

print(f"[+] Pickling best classifiers for {emotions}...")
pickle.dump(best_estimators, open(f"grid/best_classifiers.pickle", "wb"))
