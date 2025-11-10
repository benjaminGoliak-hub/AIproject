# Also re-doing this with classes
import pickle
import numpy as np
import torch
from torch import nn, optim
from numpy._typing import NDArray
from globals import CAPTURED_KEYS, PROGRAM_TTYPE, DEVICE

class PairDataset:
    # Get the data from files
    def __init__(self, files: list[str]):
        print(f'[INFO] loading {len(files)} datasets')
        frames: list[NDArray] = []
        actions: list[NDArray] = []
        for fileName in files:
            with open(fileName, 'rb') as File:
                frameData, actionData = pickle.load(File)
                frames += frameData
                actions += actionData
        self.frames = np.concatenate(frames)
        self.actions = np.concatenate(actions)
        print('[INFO] Files loaded')
    
    def __len__(self):
        return len(self.frames)
    
    # Gets a list of the data converted to tensors
    def getTensors(self):
        frames = [torch.tensor(frame, dtype=PROGRAM_TTYPE).unsqueeze(0) for frame in self.frames]
        actions = [torch.tensor(action, dtype=PROGRAM_TTYPE).unsqueeze(0) for action in self.actions]
        return frames, actions

class BCNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # Recommended shape for a network
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 8, stride=4), nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2), nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=1), nn.ReLU(),
            nn.Flatten()
        )
        self.fc = nn.Sequential(
            nn.Linear(3136, 512), nn.ReLU(),
            nn.Linear(512, len(CAPTURED_KEYS)), nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.fc(self.conv(x))

# Trains the network
def train_bc(model: BCNetwork, dataLoader: PairDataset, epochs: int):
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCELoss()
    frames, actions = dataLoader.getTensors()
    for epoch in range(epochs):
        losses = []
        for i in range(len(frames)):
            frame, action = frames[i], actions[i]
            frame, action = frame.to(DEVICE), action.to(DEVICE)
            preds = model(frame)
            loss = criterion(preds, actions)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
        print(f'[EPOCH {epoch+1}] Loss: {np.mean(losses):.4f}')
