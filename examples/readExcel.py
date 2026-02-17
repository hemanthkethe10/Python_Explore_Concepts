#/Users/hemanthk/Repos/Python
import pandas as pd

df = pd.read_csv('/Users/hemanthk/Repos/Python/Financial Applications(capabilities mapped).csv', encoding='utf-8')
products_scape_dict = df.to_dict(orient='records')
print(products_scape_dict)
# print(criterias_string)