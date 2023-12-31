import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../../AIorNot/csv/ResultsAIorNotFake.csv')

# total entry foreach model
total_counts = df.groupby('Model').size()

# dataframe percentage foreach model
percentage_df = pd.DataFrame(columns=['Model', 'Human', 'AI'])

# compute percentage foreach model
for model in total_counts.index:
    model_data = df[df['Model'] == model]

    human_percentage = model_data[model_data['Verdict'] == 'human'].shape[0] / total_counts[model]
    ai_percentage = model_data[model_data['Verdict'] == 'ai'].shape[0] / total_counts[model]

    percentage_df = pd.concat([percentage_df, pd.DataFrame({'Model': [model], 'Human': [human_percentage],
                                                            'AI': [ai_percentage]})], ignore_index=True)

# sort percentage dataframe
percentage_df = percentage_df.sort_values(by='AI', ascending=True)

# plot
fig, ax = plt.subplots(figsize=(12, 9))
bar_width = 0.35
models = percentage_df['Model']
bar_positions = range(len(models))

human_bars = ax.barh(bar_positions, percentage_df['Human'], bar_width, label='Human')
ai_bars = ax.barh(bar_positions, percentage_df['AI'], bar_width, left=percentage_df['Human'], label='AI')

ax.set_xlabel('Percentuale (0-1)', fontsize=14)
ax.set_yticks(bar_positions)
ax.set_yticklabels(models, fontsize=14)
ax.set_title('Percentuale dei verdetti per ogni modello (AIorNot)', fontsize=16)
ax.legend(fontsize=14)
ax.tick_params(axis='x', labelsize=14)

plt.show()
