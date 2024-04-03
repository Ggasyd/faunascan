# Animal Species Classification by Sound Project

This project utilizes similarity search to classify sounds made by different animal species. Currently, the model focuses on distinguishing between three main categories: dogs, cats, and birds. The aim is to enable rapid and accurate species identification from an audio recording, which can be useful for ecological, educational, or leisure applications.

## Installation
You need to have Python version 3.9 installed on your computer. To avoid dependency issues, it is recommended to work within a virtual environment and install all dependencies there. To use a virtual environment, install Anaconda on your computer. Then open the Anaconda prompt and execute the following command to create a virtual environment:
```
conda create -n env_name python=3.9
```
replacing env_name with the name of your environment.

Then execute the following command to activate the virtual environment.
```
conda activate env_name
```

Navigate to the project folder. You can install the necessary dependencies for the project to run properly via pip by executing:

```
pip install -r requirements.txt
```

## Usage
First, ensure that the paths to the "noms_animaux.txt" file and "animals.index" on your local computer are correctly configured in the script at the "chemin_noms_animaux" and "index_path" variables. To start the Gradio user interface and classify animal sounds, execute the command:

```
python hubert.py
```
Once on the user interface, upload an audio file of the animal you wish to classify. The system will return the species classification with the associated probability.

### Adding New Sounds

To add a new sound to the database:
1. Use the `add_index` file by executing the command:
```
python add_index.py path_to_audio_to_add
```
2. The script will update the index and the list of animal names

## Explanation of Different Functions
There are two main functions in this script, the animal_classification function and the add_in_index function. The animal_classification function is for classifying animals from sounds. It takes a .wav audio file as a parameter. To use it, execute the following command:
```
python animal_classification.py path_to_audio_to_add
```
The add_in_index function is used to add a new sound to the database to improve the quality of our qualification. To use it, execute the following command:
```
python add_index.py "path_to_audio_to_add"
```