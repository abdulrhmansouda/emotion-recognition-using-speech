import soundfile
import librosa
import numpy as np
import pickle
import os
from convert_wavs import convert_audio


AVAILABLE_EMOTIONS = {
    "neutral",
    "calm",
    "happy",
    "sad",
    "angry",
    "fear",
    "disgust",
    "ps", # pleasant surprised
    "boredom"
}


def get_label(audio_config):
    """
    Returns a label corresponding to the selected audio features.

    Args:
    - audio_config (dict): a dictionary containing the configuration of the audio features to be extracted.

    Returns:
    - label (str): a string representing the selected audio features.
    """

    # Define a list of available features
    features = ["mfcc", "chroma", "mel", "contrast", "tonnetz"]

    # Initialize an empty label
    label = ""

    # Iterate through the available features
    for feature in features:

        # Check if the feature is selected in the audio config
        if audio_config[feature]:

            # Add the feature to the label
            label += f"{feature}-"

    # Remove the trailing dash and return the label
    return label.rstrip("-")

def get_dropout_str(dropout, n_layers=3):
    """Returns a string representation of dropout values.

    Args:
        dropout (float or list): Dropout value(s).
        n_layers (int, optional): Number of layers to apply dropout to. Defaults to 3.

    Returns:
        str: String representation of dropout values.
    """
    if isinstance(dropout, list):
        return "_".join([str(d) for d in dropout])
    elif isinstance(dropout, float):
        return "_".join([str(dropout) for _ in range(n_layers)])

def get_first_letters(emotions):
    """Returns the first letter of each emotion in a sorted, capitalized string.
    
    Args:
    - emotions: list of emotions
    
    Returns:
    - str: string of first letters of emotions
    """
    first_letters = [e[0].upper() for e in emotions]
    return "".join(sorted(first_letters))

def extract_feature(file_name, mfcc=True, chroma=True, mel=True, contrast=True, tonnetz=True):
    """
    Extract feature from audio file `file_name`
    Features supported:
        - MFCC (mfcc)
        - Chroma (chroma)
        - MEL Spectrogram Frequency (mel)
        - Contrast (contrast)
        - Tonnetz (tonnetz)
    Usage example: `features = extract_feature(path, mel=True, mfcc=True)`
    """
    # Check if file format is supported
    try:
        with soundfile.SoundFile(file_name) as sound_file:
            pass
    except RuntimeError:
        # If file format is not supported, convert it to 16000 sample rate & mono channel using ffmpeg
        # Get the file name and directory
        basename = os.path.basename(file_name)
        dirname = os.path.dirname(file_name)
        name, ext = os.path.splitext(basename)
        new_basename = f"{name}_c.wav"
        new_filename = os.path.join(dirname, new_basename)
        # Convert the file
        v = convert_audio(file_name, new_filename)
        if v:
            raise NotImplementedError("Converting the audio files failed, make sure `ffmpeg` is installed in your machine and added to PATH.")
    else:
        new_filename = file_name

    # Read the audio file
    with soundfile.SoundFile(new_filename) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))

        result = []
        if mfcc:
            # Compute MFCC
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result.append(mfccs)
        if chroma:
            # Compute chroma feature
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result.append(chroma)
        if mel:
            # Compute MEL spectrogram feature
            mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)
            result.append(mel)
        if contrast:
            # Compute spectral contrast feature
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
            result.append(contrast)
        if tonnetz:
            # Compute tonnetz feature
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
            result.append(tonnetz)

    # Concatenate the features and return
    return np.concatenate(result)

def get_best_estimators(is_classification=True):
    """
    Load the best estimators that are saved in pickled format in the "grid" folder.
    
    Parameters:
        is_classification (bool): Specifies whether to load the best classifiers or regressors.
    
    Returns:
        A dictionary containing the best estimator(s) for the given problem type.
    """
    if is_classification:
        with open("grid/best_classifiers.pickle", "rb") as f:
            best_estimators = pickle.load(f)
    else:
        with open("grid/best_regressors.pickle", "rb") as f:
            best_estimators = pickle.load(f)
            
    return best_estimators

def get_audio_config(features_list):
    """
    Converts a list of features into a dictionary understandable by
    `data_extractor.AudioExtractor` class
    """
    audio_config = {'mfcc': False, 'chroma': False, 'mel': False, 'contrast': False, 'tonnetz': False}
    for feature in features_list:
        if feature not in audio_config:
            raise TypeError(f"Feature passed: {feature} is not recognized.")
        audio_config[feature] = True
    return audio_config
    