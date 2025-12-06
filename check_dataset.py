import pandas as pd

df = pd.read_csv('Flight_delay.csv')
delay_cols = ['CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay']
df['Delay'] = (df[delay_cols].sum(axis=1) > 30).astype(int)

print('='*50)
print('DATASET ANALYSIS')
print('='*50)
print(f'Total flights: {len(df):,}')
print(f'Delayed (1): {df["Delay"].sum():,}')
print(f'On-time (0): {(df["Delay"]==0).sum():,}')
print(f'Delay rate: {df["Delay"].mean()*100:.2f}%')
print('='*50)
