import csv
import xlrd
import openpyxl
from datetime import datetime
import re
from collections import Counter

def clean_excel(cell, datemode):
    if isinstance(cell, (float, int)) and 35000 < cell < 45000:
        date_tuple = xlrd.xldate_as_tuple(cell, datemode)
        return datetime(*date_tuple)
    else:
        return cell

def read_xls(fp):
    workbook = xlrd.open_workbook(file_contents=fp.read())
    sheet_0 = workbook.sheet_by_index(0)
    rows = []
    for row_i in range(sheet_0.nrows):
        cells = sheet_0.row_values(row_i)
        rows.append([clean_excel(cell, workbook.datemode) for cell in cells])
    return rows

def read_xlsx(fp):
    workbook = openpyxl.load_workbook(fp)
    # sheets = workbook.worksheets; sheets[0].title
    sheet_0 = workbook.get_active_sheet()
    rows = [[cell.value or '' for cell in row] for row in sheet_0.rows]
    # [map(unicode, row) for row in all_rows]
    # value=value.encode('utf8')
    return rows

def read_table(filename, fp):
    """
    A 'table' is simply a list of lists of cells (lists of cells are rows).
    Empty rows and empty columns should not be present.
    """
    if filename.endswith('.xls'):
        return read_xls(fp)
    elif filename.endswith('.xlsx'):
        return read_xlsx(fp)
    line0 = fp.readline()
    fp.seek(0)
    if len(re.findall('\t', line0)) > 0:
        return list(csv.reader(fp, delimiter='\t'))
    elif len(re.findall(',', line0)) > 0:
        return list(csv.reader(fp))
    else:
        return list(csv.reader(fp, delimiter=' '))

def guess_headers(rows):
    flat_row_0 = ' '.join(rows[0])
    if len(re.findall('email|first|last|name', flat_row_0, re.I)) > 0:
        return rows[0], rows[1:]
    else:
        # self.ctx.data = rows
        headers = []
        for cell in rows[0]:
            if '@' in cell:
                headers.append('email')
            elif ' ' in cell:
                headers.append('full_name')
            elif 'first_name' not in headers:
                headers.append('first_name')
            elif 'last_name' not in headers:
                headers.append('last_name')
            else:
                headers.append('')
        return headers, rows

def guess_users(rows):
    flat_row_0 = ' '.join(rows[0])
    # try to determine whether the first row is headers or data
    if len(re.findall('email|first|last|name', flat_row_0, re.I)) > 0:
        headers = map(rows[0], str.lower)
        data = rows[1:]
    else:
        # otherwise we go through the data and try to determine what the headers are
        # set up a "votes" list(0=x, 1=y, 2=a, ...) for each column index in the data
        max_cols = max(len(row) for row in rows)
        votes = [Counter() for col_i in range(max_cols)]
        for row in rows:
            for col_i, cell in enumerate(row):
                vote = votes[col_i]
                if '@' in cell:
                    vote['email'] += 1
                if ' ' in cell:
                    vote['full_name'] += 1
                # elif 'first_name' not in votes[col_i]:
                #     cell_guess = 'first_name'
                # elif 'last_name' not in votes[col_i]:
                #     cell_guess = 'last_name'

        # add some defaults:
        for col_i, cell_guess in enumerate(['first_name', 'last_name', 'email']):
            if col_i < len(votes):
                votes[col_i][cell_guess] += 1

        headers = [vote_counter.most_common(1)[0][0] for vote_counter in votes]
        data = rows

    # now that the headers are set, we'll interpolate the data from rows into dicts
    # note that this is the second iteration of the dat
    users = []
    for row in data:
        user = dict(zip(headers, row))

        # expand user:
        if 'full_name' in user:
            name_parts = user['full_name'].split()
            user['first_name'] = name_parts[0]
            if len(name_parts) > 2:
                user['middle_name'] = ' '.join(name_parts[1:-1])
            user['last_name'] = name_parts[-1]

        users.append(user)

    return users
