import os
import re
from pyramid.httpexceptions import HTTPFound
from confrm.handlers import BaseHandler
# from confrm.models import DBSession
# from confrm.models.user import User
from confrm.lib.table import read_table

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
            rows = read_table(filename, fp)
            flat_row_0 = ' '.join(rows[0])
            if len(re.findall('email|first|last|name', flat_row_0, re.I)) > 0:
                print 'found match'
                self.ctx.headers = rows[0]
                self.ctx.data = rows[1:]
            else:
                self.ctx.data = rows
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
                self.ctx.headers = headers

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
