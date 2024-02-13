from datetime import datetime

import pandas as pd
from pandas._testing import assert_frame_equal
from time import sleep





def update_backup(column, changes, df_column, df_backup):
    for index, row in df_column.iterrows():
        if row[f'{column}_act'] != row[f'{column}_bac']:
            row_index = df_backup.loc[df_backup[column] == row[f'{column}_bac']].index[0]
            df_backup.loc[row_index, column] = row[f'{column}_act']
            changes[0].append(row[f'{column}_bac'])
            changes[1].append(row[f'{column}_act'])
    return changes


def remove_backup(exclusion, new_rows, df_backup):
    for index, row in new_rows.iterrows():
        if not df_backup.loc[(df_backup['Name'] == row['Name']) & (df_backup['Role'] == row['Role'])].empty:
            row_index = df_backup.loc[(df_backup['Name'] == row['Name']) & (df_backup['Role'] == row['Role'])].index[0]
            df_backup.drop(row_index, inplace=True)
            exclusion.append([row['Name'], row['Role']])
    return exclusion


def insert_backup(insertions, new_rows, df_actual, df_backup):
    name, role = [], []
    for index, row in new_rows.iterrows():
        if not df_actual.loc[(df_actual['Name'] == row['Name']) & (df_actual['Role'] == row['Role'])].empty:
            insertions.append([row['Name'], row['Role']])
            name.append(row['Name'])
            role.append(row['Role'])
    data = {'Name': name, 'Role': role}
    df_data = pd.DataFrame(data).reset_index(drop=True)
    df_backup = pd.concat([df_backup, df_data], ignore_index=True)
    return insertions, df_backup


def compare_dataframes(df_act, df_bac, environment_name):
    try:
        assert_frame_equal(df_act, df_bac)
        print(f'\033[92mNo changes occurred in the {environment_name} database!\033[0m')
    except:
        print(f'\033[33mSome changes occurred onto {environment_name} database!\033[0m')
        sleep(2)

        df_name = pd.merge(df_act, df_bac, on='Name', how='inner')
        df_name = df_name.rename(columns={'Name': 'Name_act', 'Role_x': 'Role_act', 'Role_y': 'Role_bac'})

        df_role = pd.merge(df_act, df_bac, on='Role', how='inner')
        df_role = df_role.rename(columns={'Name_x': 'Name_act', 'Role': 'Role_act', 'Name_y': 'Name_bac'})

        # Creating Tuples to see save alterations
        old_values, new_values, exclusion, insertions = [], [], [], []
        changes = [old_values, new_values]
        changes = update_backup('Role', changes, df_name, df_bac)
        changes = update_backup('Name', changes, df_role, df_bac)
        # Unique values
        new_rows = pd.concat([df_bac, df_act]).drop_duplicates(keep=False)

        exclusion = remove_backup(exclusion, new_rows, df_bac)

        insertions, df_bac = insert_backup(insertions, new_rows, df_act, df_bac)
        print_differences_to_file(changes, exclusion, insertions, environment_name)


def print_differences_to_file(changes, exclusion, insertions, environment_name):
    date = datetime.now().strftime("%d-%m-%Y")
    time = datetime.now().strftime('%H:%M:%S')
    filename = f'Change_History({date}).txt'
    if environment_name == 'Korea':
        with open(f'history/{filename}', "w") as file:
            file.write(f'\n')
            file.write(f'_________________________________________________________\n')
            file.write(f'          Change Report - {date} - {time}   \n')
            file.write(f'_________________________________________________________\n')
            file.write(f'\nKorea Database:\n')
            file.write(f'\tUpdate(s):\n')
            for pair in zip(*changes):
                file.write(f'\t\t- "{pair[0]}" updated to "{pair[1]}".\n')
            file.write(f'\tDelete(s):\n')
            for e, i in exclusion:
                file.write(f'\t\t- "{e}, {i}" deleted.\n')
            file.write(f'\tInsert(s):\n')
            for e, i in exclusion:
                file.write(f'\t\t- "{e}, {i}" inserted.\n')
            file.write(f'Total Changes: {len(changes) + len(exclusion) + len(insertions)}\n')
    else:
        with open(f'history/{filename}', "a") as file:
            file.write(f'\n\nMariaDB Database:\n')
            file.write(f'\tUpdate(s):\n')
            for pair in zip(*changes):
                file.write(f'\t\t- "{pair[0]}" updated to "{pair[1]}".\n')
            file.write(f'\tDelete(s):\n')
            for e, i in exclusion:
                file.write(f'\t\t- "{e}, {i}" deleted.\n')
            file.write(f'\tInsert(s):\n')
            for e, i in exclusion:
                file.write(f'\t\t- "{e}, {i}" inserted.\n')
            file.write(f'Total Changes: {len(changes) + len(exclusion) + len(insertions)}\n')
            print('Change History created...')


