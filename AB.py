###########################
# AB Testing & Dynamic Pricing
###########################

#Kütüphaneler import edildi.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

#veri seti Control ve Test olmak üzere iki gruba ayrıldı.
A=pd.read_excel("/Users/nHn/Desktop/ab_testing_data.xlsx", sheet_name= "Control Group")
B=pd.read_excel("/Users/nHn/Desktop/ab_testing_data.xlsx", sheet_name= "Test Group")


#gözlemler
A.head()
B.head()


############################
# Sampling
############################

pop=np.random.randint(0,20,10)
pop.mean()  # 8


np.random.seed(5)
orneklem1 = np.random.choice(a=pop, size=10)
orneklem2 = np.random.choice(a=pop, size=10)
orneklem3 = np.random.choice(a=pop, size=10)
orneklem4 = np.random.choice(a=pop, size=10)
orneklem5 = np.random.choice(a=pop, size=10)

orneklem1.mean() + orneklem2.mean() + orneklem3.mean() + orneklem4.mean() + orneklem5.mean()
# 40


############################
# Descriptive Statistics
############################

A.describe().T
B.describe().T

A.corr()
B.corr()

#eksik değer olmadığı gözlemlenmiştir.
A.isnull().sum()
B.isnull().sum()

A.mean()
B.mean()


############################
# Confidence Interval
############################

import statsmodels.stats.api as sms

#dikkate alınması gereken değişken Purchase idi. Atama yapıldı.
A= A[["Purchase"]]
B= B[["Purchase"]]


#siteye giren 100 kişiden 95 i 508 ile 593 arasında satın alma yapıyor.
sms.DescrStatsW(A["Purchase"]).tconfint_mean()

#siteye giren 100 kişiden 95 i 530 ile 633 arasında satın alma yapıyor.
sms.DescrStatsW(B["Purchase"]).tconfint_mean()



############################
# AB Testing (Bağımsız İki Örneklem T Testi)
############################


############################
# 1. Varsayım Kontrolü
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


from scipy.stats import shapiro

#Test İstatistiği = 0.9773, p-değeri = 0.5891
test_istatistigi, pvalue = shapiro(A)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))

#Test İstatistiği = 0.9589, p-değeri = 0.1541
test_istatistigi, pvalue = shapiro(B)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))

# Her iki incelemede de p-value değeri 0.05 ten büyük olduğundan H0 reddedilemez.
#Normal dağılım varsayımı sağlanmaktadır.


############################
# 1.2 Varyans Homojenligi Varsayımı
############################

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


from scipy import stats

#pvalue=0.1 olduğundan H0 reddedilemez. Varyanslar homojendir.
stats.levene(A["Purchase"],
             B["Purchase"])


############################
# 2. Hipotezin Uygulanması
############################

# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anlamlı fark yoktur.)
# H1: M1 != M2 (...vardır)

# 1.1 Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
test_istatistigi, pvalue = stats.ttest_ind(A["Purchase"],
                                           B["Purchase"],
                                           equal_var=True)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))



