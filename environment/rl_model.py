import torch
import torch.nn as nn
import numpy as np

# Определяем модель
class SLMCompatibleMLP(nn.Module):
    def __init__(self, input_dim=12, hidden_dims=[32,32], output_dim=9):
        super().__init__()
        layers = []
        prev = input_dim
        for h in hidden_dims:
            layers.append(nn.Linear(prev, h))
            layers.append(nn.Tanh())
            prev = h
        self.model = nn.Sequential(*layers)
        self.tails = nn.ModuleList([nn.Linear(prev, output_dim)])

    def forward(self, x):
        x = self.model(x)
        x = self.tails[0](x)
        return x

# Загружаем веса
model = SLMCompatibleMLP()
checkpoint = torch.load('BattleOfTeams-v0.pt', map_location='cpu')
# Если внутри checkpoint есть ключ 'net' — достаём его
state_dict = checkpoint.get('net', checkpoint)
model.load_state_dict(state_dict)
model.eval()

# Функция получения действия
def get_action(obs):
    # obs — numpy array (12,) или список
    with torch.no_grad():
        tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)  # (1,12)
        logits = model(tensor)
        action = torch.argmax(logits, dim=1).item()
    return action