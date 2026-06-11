# 🎮 Battle Of Teams — стратегия с ИИ, обученным методом подкрепления

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.12+-red.svg)](https://pytorch.org/)
[![SLM‑Lab](https://img.shields.io/badge/SLM--Lab-RL--framework-8A2BE2)](https://github.com/kengz/SLM-Lab)

**Пошаговая тактическая игра**, в которой две команды по три бойца сражаются друг с другом. Вы можете играть против **искусственного интеллекта (PvE)**, обученного с помощью **REINFORCE** (Policy Gradient), или сразиться с другом в режиме **PvP**.

![Главное окно игры](https://github.com/user-attachments/assets/8a0e4ea5-5160-4fd9-a04d-9ecd6f8223c5)

## ✨ Особенности

- ⚔️ **Два режима игры**  
  – **PvE**: бросьте вызов нейросетевому агенту, который учился на сотнях тысяч сражений.  
  – **PvP**: классический режим «друг против друга» за одним компьютером.

- 🧠 **AI на градиенте политики**  
  Агент обучался в среде **SLM-Lab** с использованием алгоритма **REINFORCE** (с центрированием наград и регуляризацией энтропии). В его распоряжении – два скрытых слоя по 128 нейронов, а наблюдение включает силу и статус каждого бойца.

<div align="center">
  <img width="25%" alt="BattleOfTeams-v1_mean_returns" src="https://github.com/user-attachments/assets/632f04f6-999b-4133-abb1-bccd90c7a020" />
  <img width="25%" alt="BattleOfTeams-v1_mean_returns_ma" src="https://github.com/user-attachments/assets/44506df6-e5d7-4f1f-9cf4-e29c827931c1" />
</div>

- 🃏 **Интуитивное управление**  
  Выбор атакующего и защитника происходит в два клика по карточкам бойцов. Подсветка и текстовый лог помогают следить за каждым ходом.

- 🎨 **Визуальная обратная связь**  
  Сила бойцов меняется в реальном времени, мёртвые юниты блокируются, а ход боя подробно логируется.

  ![Лог сражения](https://github.com/user-attachments/assets/62dba24c-0bb4-48de-8ab6-c3e08c1c87ee)

## 🛠 Технологии

Проект написан на **Python 3.12+** и использует:

| Компонент       | Технологии                                                                |
|----------------|----------------------------------------------------------------------------|
| Боевая логика  | `dataclasses`, `random`                                                    |
| Интерфейс      | `tkinter`                                                                  |
| Обучение ИИ    | `SLM-Lab` + `PyTorch` + `gymnasium`                                        |
| Графика        | `Pillow` (поддержка PNG/JPG)                                               |
| Визуализация   | Tkinter (кнопки, scrolledtext, ttk)                                        |

## 🚀 Запуск проекта

1. **Клонируйте репозиторий**  
   ```bash
   git clone https://github.com/your-username/BattleOfTeams.git
   cd BattleOfTeams
