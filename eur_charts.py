import pandas as pd
import matplotlib.pyplot as plt

# 1. Завантаження даних
eur = pd.read_csv('data/eur.csv')

# Перетворення дати у формат datetime
eur['date'] = pd.to_datetime(eur['date'])

# 2. Налаштування стилю для темної теми
plt.style.use('dark_background')

plt.figure(figsize=(12, 6), facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')

# 3. Побудова графіків (зелені відтінки на чорному тлі)
plt.plot(eur['date'], eur['rate'], label='EUR / UAH', color='#76ff03', linewidth=1.8, linestyle='--')

# 4. Оформлення графіку
plt.title('Динаміка офіційних курсів валют (2020 – 2025 рр.)', fontsize=14, fontweight='bold', color='white')
plt.xlabel('Дата', fontsize=12, color='white')
plt.ylabel('Курс (грн)', fontsize=12, color='white')

plt.legend(fontsize=12, facecolor='black', edgecolor='white', labelcolor='white')
plt.grid(True, linestyle='--', alpha=0.3, color='gray')

# Налаштування кольору осей
ax.tick_params(colors='white', which='both')
for spine in ax.spines.values():
    spine.set_color('gray')

plt.tight_layout()

# 5. Збереження та відображення
plt.savefig('data/eur.png', dpi=300, facecolor='black')