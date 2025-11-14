# Imm-Mirror an CNN Behavioral Cloning Neural Network
CS-5820 Final project
Authors: Ben Goliak, Jack Herrington, John Yoshida

## Project outline
This project provides a trainable CNN that can be conrolled in the background and quickly trained to mimic user inputs for simple games. 

## Requirements
using pip you will need the following python packages
* PyTorch (torch)
* mss
* Pillow
* pynput

## Use intstructions
To start the program run main.py \n
These are the default controls for the program: \n
'=' - Start capturing a recording session \n
'-' - End current recording session \n
'\\' - Train model on saved recordings \n
';' - Enter model control mode \n
'esc' - Exit model control mode \n
'backspace' - Delete all trained data \n

> You can load a saved model with the ';' command \n
> but to re-train a new model from the ground up, restart the program and train it using the '\\' command \n
> Commands will also be queued during blocking states (recording, training, inference) so take note not to queue actions \n

to change the keys the model is trained to interact with, edit the CAPTURED_KEYS variable in the globals.py file (note you will need to delete all recordings)

## How it works
The program uses 'behavioral cloning (BC)' to learn from the recordings. Instead of seeking to understand how the recorded game works, the algorithim learns to associate the frames with the recorded actions of the player. This makes it easy to train a somewhat effective system, with the downside of it having little ability to adapt to new states and correct its play when mistakes are made




