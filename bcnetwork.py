# Also re-doing this with classes
import pickle
import numpy as np
import torch
import torch.nn as nn
from numpy._typing import NDArray
from globals import CAPTURED_KEYS, PROGRAM_TTYPE

class PairDataset:
    # Get the data from files
    def __init__(self, files: list[str]):
        frames: list[NDArray] = []
        actions: list[NDArray] = []
        for fileName in files:
            with open(fileName, 'rb') as File:
                frameData, actionData = pickle.load(File)
                frames += frameData
                actions += actionData
        self.frames = np.concatenate(frames)
        self.actions = np.concatenate(actions)
    
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


# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import datamanager

# # 1. Define the policy network
# class PolicyNet(nn.Module):
#     def __init__(self, state_dim, action_dim):
#         super(PolicyNet, self).__init__()
#         self.con1 = nn.Linear(state_dim, 512)
#         self.con2 = nn.Linear(512, 128)
#         self.relu = nn.ReLU()
#         self.lg1 = nn.Linear(128, 128)
#         self.lg2 = nn.Linear(128, 64)
#         self.lg3 = nn.Linear(64, action_dim)

#     def forward(self, x):
#         x = self.con1(x)
#         x = self.relu(self.con2(x))
#         x = self.relu(self.lg1(x))
#         x = self.relu(self.lg2(x))
#         x = self.relu(self.lg3(x))
#         return x

# # 2. Prepare dummy expert data (replace with your actual data)

# expert_states, expert_actions = datamanager.collectPairs(int(1000/15), 60)
# print("input capture done")

# expert_states = torch.from_numpy(expert_states).float()
# expert_actions = torch.from_numpy(expert_actions).float()
# print(expert_states.size())
# dataset = TensorDataset(expert_states, expert_actions)
# dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# # 3. Initialize model, loss, and optimizer
# state_dim = int(datamanager.SCALE[0] * datamanager.SCALE[1])
# action_dim = int(len(datamanager.KEYS) * 2) 
# model = PolicyNet(state_dim, action_dim)
# criterion = nn.MSELoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)

# # 4. Training loop
# num_epochs = 50
# for epoch in range(num_epochs):
#     for states, actions in dataloader:
#         optimizer.zero_grad()
#         predicted_actions = model(states)
#         loss = criterion(predicted_actions, actions)
#         loss.backward()
#         optimizer.step()
#     print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")

# # 5. Inference (example)
# new_state = expert_states[4]
# predicted_action = model(new_state)
# print(f"Predicted action for new state: {predicted_action.detach().numpy()}")