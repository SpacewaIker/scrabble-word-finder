# import re

# pattern = re.compile('AS[A-Z]{1}DR')


# condition = (
#     lambda _: True if pattern.fullmatch(_) is not None else False
# )

# print(
#     condition('ASFDR')
# )

import pandas as pd

df = pd.DataFrame(
    [1, 2, 3, 4, 5],
    columns=['Numbers']
)

df_app = pd.DataFrame(
    [1, 2, 3],
    columns=['Numbers']
)

df1 = df.append(
    df_app,
    ignore_index=True,
)

print(df1)

df1 = df1.drop_duplicates()

print(df1)
