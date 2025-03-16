import pandas

a = {1: [1, 2, 3], 2: [4, 5, 6]}
b = {1: [7, 8, 9], 2: [10, 11, 12]}

df1 = pandas.DataFrame(a)
df2 = pandas.DataFrame(b)

df = pandas.concat([df1, df2], axis=0)
print(df)
