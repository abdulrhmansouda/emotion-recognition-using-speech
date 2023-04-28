from sklearn.neural_network import MLPClassifier

classifier_model = MLPClassifier()
# hyper_parameter = {
#         'hidden_layer_sizes': [(200,), (300,), (400,), (128, 128), (256, 256)],
#         'alpha': [0.001, 0.005, 0.01],
#         'batch_size': [128, 256, 512, 1024],
#         'learning_rate': ['constant', 'adaptive'],
#         'max_iter': [200, 300, 400, 500]
#     }
hyper_parameter = {
        'hidden_layer_sizes': [(400,)],
        'alpha': [0.005],
        'batch_size': [1024],
        'learning_rate': ['constant'],
        'max_iter': [200]
    }

# {'alpha': 0.005, 'batch_size': 1024, 'hidden_layer_sizes': (400,), 'learning_rate': 'constant', 'max_iter': 200}

# emotion classes you want to perform grid search on
emotions = ['sad', 'neutral', 'happy', 'calm',
            'angry', 'fear', 'disgust', 'ps', 'boredom']

# ps = (pleasant surprise)

dataset = {
    'tess_ravdess': True,
    'emodb': True,
    'custom_db': True
}


# number of parallel jobs during the grid search
n_jobs = 4

# for warning message
verbose = 1

balance = True