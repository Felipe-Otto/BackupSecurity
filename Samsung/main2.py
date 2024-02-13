import pandas as pd
from pandas._testing import assert_frame_equal

from utils import update_backup, remove_backup, insert_backup, compare_dataframes

'''
Simulating that these dataframes were created from data extracted from Korea and the Database simultaneously
'''
# Creating Korea dataframe
data_korea = {'Name': ['Alice Park', 'Charlie Kang', 'Anna Choi', 'Mudei HEhe', 'Grace Shin',
                       'Henry Yoon', 'Adicionei hehe'],
              'Role': ['Data Analyst', 'Project Manager', 'Mudei hehe',
                       'Front-end Developer', 'HR Manager', 'Systems Analyst', 'add emprego novo']}

df_korea_actual = pd.DataFrame(data_korea).reset_index(drop=True)

# Creating backup dataframe
data_mariadb = {'Name': ['Sophia Kim', 'David Lee', 'Emily Park', 'William Choi', 'Olivia Kim', 'Novo'],
               'Role': ['Business Analyst', 'Full-stack Developer', 'Data Analyst', 'Project Manager',
                        'Systems Analyst', 'Novo']}

df_mariadb_actual = pd.DataFrame(data_mariadb).reset_index(drop=True)

'''Ver isso depois. Essas transformações ocorrerão por ultimo'''
# Making backup from two datframes for next operations
# df_korea.to_parquet('dataframes/df_korea_backup.parquet', index=False)
# df_mariadb_actual.to_parquet('dataframes/df_mariadb_backup.parquet', index=False)

'''
Analyzing the most recent backups of both the Korean data and the database, converting them into a dataframe to identify 
and understand recent changes.
'''
# Creating Korea backup dataframe
df_korea_backup = pd.read_parquet('dataframes/df_korea_backup.parquet')
# Creating database backup dataframe
df_mariadb_backup = pd.read_parquet('dataframes/df_mariadb_backup.parquet')

# Finding alterations onto korea datframe:
compare_dataframes(df_korea_actual, df_korea_backup, 'Korea')
compare_dataframes(df_mariadb_actual, df_mariadb_backup, 'MariaDB')
# Lines difference up:




# Creating a datframe with datas that has the same name

