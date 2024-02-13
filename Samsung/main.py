from time import sleep

import pandas as pd
from pandas.testing import assert_frame_equal
from tabulate import tabulate

# Creating Dataframes

# Korea dataframe
# Korea dataframe with different sizes
data_korea = {'Name': ['Alice Parkinton', 'John Kim', 'Bob Lee', 'Charlie Kang', 'Anna Choi', 'Daniel Lee', 'Grace Shin',
                       'Henry Yoon'],
              'Role': ['Data Analyst', 'Software Engineer', 'Web Developer', 'Project Manager', 'Quality Analyst',
                       'Front-end Developer', 'HR Manager', 'Systems Analyst']}

df_korea = pd.DataFrame(data_korea).reset_index(drop=True)

# Backup dataframe
data_backup = {'Name': ['Sophia Kim', 'David Lee', 'Emily Park', 'William Choi', 'Olivia Kim', 'Michael Lee'],
               'Role': ['Business Analyst', 'Full-stack Developer', 'Data Analyst', 'Project Manager',
                        'Systems Analyst', 'Marketing Specialist']}

df_backup = pd.DataFrame(data_backup).reset_index(drop=True)

# Comparing dataframes content
try:
    assert_frame_equal(df_korea, df_backup)

except AssertionError as e:
    print('\033[93mUpdate required...\033[m\n')
    sleep(2)
    # Handling shape mismatch error
    if 'DataFrame shape mismatch' in str(e):
        # Printing a warning about the shape difference
        size = (df_korea.shape[0] - df_backup.shape[0])
        print(f"Actual Korea dataframe has {abs(size)} {'more' if size > 0 else 'less' if size < 0 else 'same'} "
              f"lines than backup\'s!")
        sleep(2)

    # Handling content difference error
    if 'are different' in str(e):
        # Finding differences between dataframes
        merged = pd.merge(df_korea, df_backup, how='outer', indicator=True).loc[lambda x: x['_merge'] != 'both']

        # Duplicating Backup dataframe
        df_backup_copy = df_backup.copy()

        print(f'Updating backup\'s dataframe with Korea data:')
        sleep(2)
        # Updating altered fields in the Database
        for index_kor, row_kor in df_korea.iterrows():
            for index_bac, row_bac in df_backup.iterrows():
                if row_kor['Name'] == row_bac['Name'] or row_kor['Role'] == row_bac['Role']:
                    if row_kor['Name'] == row_bac['Name']:
                        print(f'- {row_bac["Role"]} --> \'\033[32m{row_kor["Role"]}\033[m\' '
                              f'(ln.{index_bac + 1}).')
                        df_backup.loc[index_bac] = df_korea.loc[index_kor]
                        sleep(0.5)
                    else:
                        print(f'- {row_bac["Name"]} --> \'\033[32m{row_kor["Name"]}\033[m\' '
                              f'(ln.{index_bac + 1}).')
                        df_backup.loc[index_bac] = df_korea.loc[index_kor]
                        sleep(0.5)
                    break

        # Deleting rows inserted in the Database
        print('\nRemoving extra lines (inserted in the database manually):')
        sleep(2)
        df_support = pd.merge(df_backup_copy, df_backup, on=['Name', 'Role'], how='inner')
        for index_sup, row_sup in df_support.iterrows():
            for index_bac, row_bac in df_backup.iterrows():
                if [row_sup['Name'], row_sup['Role']] == [row_bac['Name'], row_bac['Role']]:
                    df_backup = df_backup.drop(index=index_bac)
                    print(f'- \033[31m{row_sup["Name"]}, {row_sup["Role"]}\033[m excluded (ln.{index_bac + 1}).')
                    sleep(0.5)
                    break

        # Adding new Korea data to the backup dataframe
        print('\nAdding new data from Korea:')
        sleep(2)
        new_korea_data_df = pd.merge(df_korea, df_backup, how='outer', indicator=True).query(
            '_merge == "left_only"').drop(
            '_merge', axis=1)
        for index_kor, row_kor in new_korea_data_df.iterrows():
            print(f'- \033[32m{row_kor["Name"]}, {row_kor["Role"]}\033[m added.')
            sleep(0.5)

        df_backup = pd.concat([df_backup, new_korea_data_df], ignore_index=True)

        # Creating a sorted backup dataframe
        Name = []
        Role = []

        # Sorting dataframe like Korea's
        print('\nSorting backup dataframe...')
        for index_kor, row_kor in df_korea.iterrows():
            for index_bac, row_bac in df_backup.iterrows():
                if [row_kor['Name'], row_kor['Role']] == [row_bac['Name'], row_bac['Role']]:
                    Name.append(row_bac['Name'])
                    Role.append(row_bac['Role'])
                    break

        sorted_backup = {'Name': Name, 'Role': Role}
        df_backup = pd.DataFrame(sorted_backup)

# Asserting again for confirmation
assert_frame_equal(df_korea, df_backup)
pd.set_option('display.width', 200)

print(f'Korea dataframe:\n')
print(tabulate(df_korea, headers='keys', tablefmt='fancy_grid'))
print(f'Backup dataframe:\n')
print(tabulate(df_backup, headers='keys', tablefmt='fancy_grid'))
