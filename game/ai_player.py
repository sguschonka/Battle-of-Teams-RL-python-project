import torch
import numpy as np
import pickle


class AIPlayer:
    def __init__(self, checkpoint_path: str, obs_rms_path: str = None):
        self.model = self._load_model(checkpoint_path)
        self.obs_rms = self._load_obs_rms(obs_rms_path) if obs_rms_path else None

    def _load_model(self, path):
        class BattleMLP(torch.nn.Module):
            def __init__(
                self, input_dim=12, hidden_dims=[128, 128], output_dim=9
            ):  # For BattleOfTeams-v0 32,32
                super().__init__()
                layers = []
                prev = input_dim
                for h in hidden_dims:
                    layers.append(torch.nn.Linear(prev, h))
                    layers.append(torch.nn.Tanh())
                    prev = h
                self.model = torch.nn.Sequential(*layers)
                self.tails = torch.nn.ModuleList([torch.nn.Linear(prev, output_dim)])

            def forward(self, x):
                x = self.model(x)
                x = self.tails[0](x)
                return x

        model = BattleMLP()
        checkpoint = torch.load(path, map_location="cpu")
        state_dict = checkpoint.get("net", checkpoint)
        model.load_state_dict(state_dict)
        model.eval()
        return model

    def _load_obs_rms(self, path):
        with open(path, "rb") as f:
            rms = pickle.load(f)
        return rms

    def get_action(
        self, observation: list
    ) -> int:  # observation: list of 12 numbers (strengths & alive)
        obs = np.array(observation, dtype=np.float32)
        if self.obs_rms is not None:
            mean = self.obs_rms.mean
            std = self.obs_rms.std
            obs = (obs - mean) / (std + 1e-8)
        with torch.no_grad():
            tensor = torch.from_numpy(obs).unsqueeze(0)
            logits = self.model(tensor)
            # Can use argmax (determine) or sample (stochastically)
            action = torch.argmax(logits, dim=1).item()
        return action
