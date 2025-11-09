# Will implement the neural network
# 0 clue how to do this but you can help
# https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html
# https://medium.com/@sthanikamsanthosh1994/imitation-learning-behavioral-cloning-using-pytorch-d5013404a9e5

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import datamanager

# 1. Define the policy network
class PolicyNet(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(PolicyNet, self).__init__()
        self.fc1 = nn.Linear(state_dim, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, action_dim)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 2. Prepare dummy expert data (replace with your actual data)

expert_states, expert_actions = datamanager.collectPairs(int(1000/15), 60)
print("input capture done")

expert_states = torch.from_numpy(expert_states).float()
expert_actions = torch.from_numpy(expert_actions).float()
print(expert_states.size())
dataset = TensorDataset(expert_states, expert_actions)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 3. Initialize model, loss, and optimizer
state_dim = int(datamanager.SCALE[0] * datamanager.SCALE[1])
action_dim = int(len(datamanager.KEYS) * 2) 
model = PolicyNet(state_dim, action_dim)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 4. Training loop
num_epochs = 10
for epoch in range(num_epochs):
    for states, actions in dataloader:
        optimizer.zero_grad()
        predicted_actions = model(states)
        loss = criterion(predicted_actions, actions)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")

# 5. Inference (example)
new_state = expert_states[4]
predicted_action = model(new_state)
print(f"Predicted action for new state: {predicted_action.detach().numpy()}")