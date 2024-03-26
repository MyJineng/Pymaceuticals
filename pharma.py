import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st

pd.set_option('display.max_columns', None)

csv1 = "data/Mouse_metadata.csv"
csv2 = "data/Study_results.csv"
df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)
df = pd.merge(df1, df2, how="right")
print(f'Unique mice: {df["Mouse ID"].nunique()}')
dfdup = df.loc[df.duplicated(subset=['Mouse ID', 'Timepoint', ]), 'Mouse ID'].unique()
print(dfdup)
dfsearch = df.loc[df["Mouse ID"] == "g989", :]
print(dfsearch)
df.index = df["Mouse ID"]
df = df.drop("g989")
print(f'Unique mice: {df["Mouse ID"].nunique()}')

mean = df.groupby("Drug Regimen")["Tumor Volume (mm3)"].mean()
median = df.groupby('Drug Regimen')["Tumor Volume (mm3)"].median()
variance = df.groupby('Drug Regimen')["Tumor Volume (mm3)"].var()
std = df.groupby('Drug Regimen')["Tumor Volume (mm3)"].std()
sem = df.groupby('Drug Regimen')["Tumor Volume (mm3)"].mean()

sum = pd.DataFrame({"Mean Tumor Volume": mean, "Median Tumor Volume": median,
                    "Tumor Volume Variance": variance, "Tumor Volume Std. Dev.": std,
                    "Tumor Volume Std. Err.": sem})
print(sum)
other_sum = df.groupby(['Drug Regimen'])[['Tumor Volume (mm3)']].agg(['count', 'sum', 'mean', 'median', 'var', 'std', 'sem'])
print(other_sum)

x_axis = df.groupby(['Drug Regimen'])["Timepoint"].count()
plot = x_axis.plot.bar(color='tab:red')
plt.xlabel("Drug Type")
plt.ylabel("Number of Timepoints")
plt.title("Timepoints by Drug Type")
plt.show()

x_axis = x_axis.index.values
y_axis = df.groupby(['Drug Regimen'])["Timepoint"].count()
plt.bar(x_axis, y_axis, color='tab:red', alpha=1, align='center')
plt.xlabel("Drug Type")
plt.ylabel("Number of Timepoints")
plt.xticks(rotation="vertical")
plt.title("Timepoints by Drug Type")
plt.show()

sex = df["Sex"].value_counts()
sex.plot.pie(autopct= "%1.1f%%")
plt.title("Sex Distribution")
plt.show()

male = (round(sex[0]/(sex[0] + sex[1]) * 100))
female = (round(sex[1]/(sex[0] + sex[1]) * 100))
labels = ['Male', 'Female']
sizes = [male, female]
plot = sex.plot.pie(y='Total Count', autopct="%1.1f%%")
plt.title("Sex Distribution")
plt.show()

df = pd.merge(df1, df2, how="left")
df3 = df.groupby(["Mouse ID"])["Timepoint"].max()
df3 = df3.reset_index()
df3 = pd.merge(df, df3, on=['Mouse ID','Timepoint'], how="left")

drug_search = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']
drugs = {'Capomulin': [], 'Ramicane': [], 'Infubinol': [], 'Ceftamin': []}
for drug in drug_search:
    for mouse in df3.index:
        if df3.iloc[mouse]['Drug Regimen'] == drug:
            drugs[drug].append(df3.iloc[mouse]['Tumor Volume (mm3)'])

dft = pd.DataFrame.from_dict(drugs, orient='index')
dft = dft.transpose()
dfd = dft.describe()
for drug in drug_search:
    iqr = ((dfd.loc['75%'][drug]) - (dfd.loc['25%'][drug]))
    lower_bound = (dfd.loc['25%'][drug] - (1.5 * iqr))
    upper_bound = (dfd.loc['75%'][drug] + (1.5 * iqr))
    print(f'{drug}: IQR: {iqr}, upper: {upper_bound}, lower: {lower_bound}')
    outliers = dft.loc[(dft[drug] <= lower_bound) | (dft[drug] >= upper_bound)]
    print(outliers)
