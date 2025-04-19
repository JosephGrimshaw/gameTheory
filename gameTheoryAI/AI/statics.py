import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import torch

trainTestcsv = './AI/hawkDoveData.csv'
data = pd.read_csv(trainTestcsv)
train_data_csv, test_data_csv = train_test_split(data, test_size=0.2, random_state=42)

features = data.columns[:5]
mean = train_data_csv[features].mean()
std = train_data_csv[features].std()

train_data_csv[features] = (train_data_csv[features] - mean) / std
test_data_csv[features] = (test_data_csv[features] - mean) / std

class Dataset(Dataset):
    def __init__(self, csv):
        self.data = csv
        self.len = self.data.shape[0]

    def __len__(self):
        return self.len
    
    def __getitem__(self, idx):
        features = torch.tensor(self.data.iloc[idx, :5].values, dtype=torch.float32)
        label = torch.tensor(self.data.iloc[idx, 5], dtype=torch.float32).view(1)
        return features, label

class Model(nn.Module):
    def __init__(self, hLayers, layerNeurones, dropoutP=0.1):
        super(Model, self).__init__()
        layers = []
        layers.append(nn.Linear(5,layerNeurones))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(dropoutP))
        for layer in range(hLayers):
            layers.append(nn.Linear(layerNeurones,layerNeurones))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropoutP))
        layers.append(nn.Linear(layerNeurones, 1))
        self.compute = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.compute(x)


train_data = Dataset(train_data_csv)
test_data = Dataset(test_data_csv)

train_loader = DataLoader(train_data, batch_size=51, shuffle=True)
test_loader = DataLoader(test_data, batch_size=51)