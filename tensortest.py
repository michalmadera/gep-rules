# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 20:09:45 2021

@author: michalm
"""
import tensorflow as tf
import pandas as pd

a = tf.constant([1,2,3])
b = tf.constant([4,5,6])

df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})


data = pd.DataFrame()
col = 'a'
x = tf.constant(df[col].values)

for col in df.columns:
    x = tf.constant(df[col].values)
    print(x)
    data = data.append({""+col:x},ignore_index=True)

data = [tf.constant([1,2,3]), tf.constant([4,5,6])]

df.columns.get_loc('b')

print('aaaa', eval("data[df.columns.get_loc('a')] * data[df.columns.get_loc('b')]"))


