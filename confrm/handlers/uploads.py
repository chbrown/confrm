import os
import csv
import xlrd
import openpyxl
from pyramid.httpexceptions import HTTPFound
from confrm.handlers import BaseHandler
# from confrm.models import DBSession
# from confrm.models.user import User
import re

def read_xls(fp):
    workbook = xlrd.open_workbook(fp)
    sheet_0 = workbook.sheet_by_index(0)
    row_0 = sheet_0.row_values(0)
    rows = []
    for row_i in range(1, sheet_0.nrows):
        rows.append(sheet_0.row_values(row_i))
    return row_0, rows

def read_xlsx(fp):
    workbook = openpyxl.load_workbook(fp)
    # sheets = workbook.worksheets; sheets[0].title
    sheet_0 = workbook.get_active_sheet()
    all_rows = [[cell.value or '' for cell in row] for row in sheet_0.rows]
    # [map(unicode, row) for row in all_rows]
    row_0 = all_rows[0]
    rows = all_rows[1:]

    # value=value.encode('utf8')
    return row_0, rows

def read_csv(csv_fp):
    row_0 = csv_fp.next()
    rows = list(csv_fp)
    return row_0, rows

def read_table(filename, fp):
    """
    A 'table' is a list of headers, and a list of rows.
    Empty rows and empty columns should not be present.
    """
    if filename.endswith('.xls'):
        return read_xls(fp)
    elif filename.endswith('.xlsx'):
        return read_xlsx(fp)
    line0 = fp.readline()
    fp.seek(0)
    if len(re.findall('\t', line0)) > 0:
        return read_csv(csv.reader(fp, delimiter='\t'))
    elif len(re.findall(',', line0)) > 0:
        return read_csv(csv.reader(fp))
    else:
        return read_csv(csv.reader(fp, delimiter=' '))

class UploadHandler(BaseHandler):
    """
    1a. The user goes to /uploads/index to upload a file, csv or xls
    1b. They POST their file with jQuery-File-Upload to /uploads/create
    2.  The user goes to /uploads/index to view the uploaded files
    3a. They pick one, going to /uploads/edit?filename=abcdef.xls
    3b. On that page, they can set mappings, functions, cleaners, etc.
    4.  Their settings are saved as an "upload_filter," and they go to /uploads/show?filename=abcdef.xls, to preview the way their data will look like after their filter is applied, resulting in how my app will show it.
    """
    base = 'uploads'

    def __route__(self, request):
        # super(UploadHandler, self).__init__(request)
        # return Response('hi')

        args = request.matchdict['args']
        self.path = [self.base, args[0]]
        getattr(self, args[0])(*args[1:])

    def index(self, *args):
        filenames = os.listdir(self.localdir)
        self.ctx.uploads = [filename for filename in filenames if not filename.startswith('.')]

    def show(self, filename):
        filepath = '%s/%s' % (self.localdir, filename)
        with open(filepath) as fp:
            row_0, rows = read_table(filename, fp)
            self.ctx.headers = row_0
            self.ctx.data = rows

    def create(self, *args):
        self.format = 'json'

        upload = self.request.params['files[]']
        localpath = '%s/%s' % (self.localdir, upload.filename)
        with open(localpath, 'wb') as fp:
            file_contents = upload.file.read()
            file_size = len(file_contents)
            fp.write(file_contents)

        # shutil.copyfileobj(f.file, fdst)

        resource_url = '/uploads/show/%s' % upload.filename
        res = dict(
            name=upload.filename,
            size=file_size,
            url=resource_url,
            delete_url=resource_url,
            delete_type='DELETE'
        )
        self.ctx = [res]

    def delete(self, filename):
        filename = filename.replace('..', '')
        os.remove('%s/%s' % (self.localdir, filename))

        self.ctx.message = "%s deleted." % filename
        if self.request.method == 'POST':
            self.ctx.success = True
        else:
            raise HTTPFound(location='/uploads/index?message=%s' % self.ctx.message)

    @property
    def localdir(self):
        dirpath = '%s/files' % self.request.registry.settings['package_directory']
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        return dirpath
