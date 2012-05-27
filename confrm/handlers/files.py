import os
from datetime import datetime
from pyramid.httpexceptions import HTTPFound
from confrm.handlers import BaseHandler
from confrm.models import DBSession, File

class FileHandler(BaseHandler):
    base = 'files'

    def index(self, *args):
        filenames = os.listdir(self.localdir)
        self.ctx.uploads = [filename for filename in filenames if not filename.startswith('.')]

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

    def delete(self, file_id):
        file_object = DBSession.query(File).get(file_id)
        file_object.deleted = datetime.now()
        DBSession.flush()

        message = "%s deleted." % file_object.filename
        if self.request.method == 'GET':
            raise HTTPFound(location='/uploads/index?message=%s' % message)

        self.set_ctx(success=True, message=message)

    # @property
    # def localdir(self):
    #     dirpath = '%s/files' % self.request.registry.settings['package_directory']
    #     if not os.path.exists(dirpath):
    #         os.mkdir(dirpath)
    #     return dirpath
