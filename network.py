import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

device = torch.accelerator.current_accelerator() if torch.accelerator.is_available() else "cpu"
print(f"Using {device} device")