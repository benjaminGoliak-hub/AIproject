# Also re-doing this with classes
import pickle
import numpy as np
import torch
from torch import nn, optim
from numpy._typing import NDArray
from torch.utils.data import DataLoader, Dataset
from globals import CAPTURED_KEYS, CAPTURED_SCALE, PROGRAM_TTYPE, DEVICE, STACK_FRAMES

class PairDataset(Dataset):
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
        self.frames = np.stack(frames)
        self.actions = np.stack(actions)
        print('[INFO] Files loaded')
    
    def __len__(self):
        return len(self.frames)
    
    # Gets a list of the data converted to tensors
    def __getitem__(self, index):
        action = torch.tensor(self.actions[index], dtype=PROGRAM_TTYPE) # .unsqueeze(0)
        frameStack = []
        for d in STACK_FRAMES:
            frameStack.append(self.frames[max(0, index - d)])
        frameStack = np.stack(frameStack, axis=0)

        frame = torch.tensor(frameStack, dtype=PROGRAM_TTYPE)
        return frame, action

class BCNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # Recommended shape for a network
        self.conv = nn.Sequential(
            nn.Conv2d(len(STACK_FRAMES), 32, 8, stride=4), nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2), nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=1), nn.ReLU(),
            nn.Flatten()
        )
        with torch.no_grad():
            sample = torch.zeros(1, len(STACK_FRAMES), *CAPTURED_SCALE)
            out = self.conv(sample).view(1, -1)
            n_features = out.numel()
        
        self.fc = nn.Sequential(
            nn.Linear(n_features, 512), nn.ReLU(),
            nn.Linear(512, len(CAPTURED_KEYS)), nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.fc(self.conv(x))

# Trains the network
def train_bc(model: BCNetwork, dataLoader: DataLoader, epochs: int):
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCELoss()
    for epoch in range(epochs):
        losses = []
        for frame, action in dataLoader:
            frame, action = frame.to(DEVICE), action.to(DEVICE)
            preds = model(frame)
            loss = criterion(preds, action)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
        print(f'[EPOCH {epoch+1}] Loss: {np.mean(losses):.4f}')
    
    torch.save(model.state_dict(), "bc_model.pth")
    print("[INFO] Model saved to bc_model.pth")
