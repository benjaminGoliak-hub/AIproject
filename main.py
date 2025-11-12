from pynput import keyboard
import torch
from datamanager import DataManager
from bcnetwork import BCNetwork, PairDataset, train_bc
from globals import DEVICE, SNIPIT_DIR
from torch.utils.data import DataLoader, Dataset
import threading
from controller import model_control
import os

def main():
    recorder = DataManager()
    model = BCNetwork().to(DEVICE)
    running = True
    print('[Directions] press \'+\' to record, \'-\' to stop, \\ to train, and \';\' to run')

    def on_press(key):
        print(key)
        try:
            if key.char == '+':
                if not recorder.isRecording:
                    threading.Thread(target=recorder.record).start()
            elif key.char == '-':
                recorder.stop()
            elif key.char == '\\':
                print('[INFO] Training Entered')
                try:
                    files = [os.path.join(SNIPIT_DIR, f) for f in os.listdir(SNIPIT_DIR) if f.endswith('.pkle')]
                except: 
                    print('[ERROR] did not create pickle directory')
                    return 
                print('[INFO] Working with files {files}')
                if not files:
                    print('[WARNING] No files found')
                    return
                dataset = PairDataset(files)
                dataLoader = DataLoader(dataset, batch_size=32, shuffle=True)
                train_bc(model, dataLoader, 10)
            elif key.char == ';':
                print('[INFO] Model training active')
                if not os.path.exists("bc_model.pth"):
                    print("[WARN] Train model first.")
                    return
                

                model.load_state_dict(torch.load("bc_model.pth", map_location=DEVICE))
                print('[INFO] Control started, press escape to quit')
                model_control(model, keyboard.Controller())
                print('[INFO] Control ended')
        except Exception as e:
            pass
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

print("Current working dir:", os.getcwd())

if __name__ == '__main__':
    main()