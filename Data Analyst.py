from numpy import loadtxt, row_stack
from numpy.lib.function_base import append
from numpy.lib.npyio import save
import pandas as pd
from openpyxl import Workbook as wb
import numpy as np
from pandas.core.reshape.pivot import pivot, pivot_table

df = pd.read_csv('payouts.csv', delimiter=',')
Country = pd.read_csv('countries.csv')
industry = pd.read_csv('industries.csv')


pais = df.merge(Country, on='merchant_id')

industria = pais.merge(industry, on='merchant_id')
industria['dollar'] = industria['amount'].divide(100)
industria['month'] = pd.to_numeric(industria['date'].str[5:7]) 

#Quarter = []
#for m in industria['month']: 
#    m //4 + 1 
#industria['Q'] = Quarter

saveC = pd.pivot_table(industria,['dollar','count'],['country'], aggfunc=np.sum, margins_name= 'Total',margins=True)
saveI = pd.pivot_table(industria,['dollar','count'],['industry'], aggfunc=np.sum,margins_name= 'Total',margins=True)
saveM = pd.pivot_table(industria,['dollar','count'],['month'], aggfunc=np.sum,margins_name= 'Total',margins=True)

writer =  pd.ExcelWriter('Analysis.xlsx')

saveC.to_excel(writer,index=True,sheet_name= 'By Country')
saveI.to_excel(writer,index=True,sheet_name= 'By Industry')
saveM.to_excel(writer,index=True,sheet_name= 'By Month')

writer.save() 
print()
