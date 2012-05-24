from confrm.handlers import BaseHandler
from confrm.models import DBSession
from confrm.models.user import User

class UploadHandler(BaseHandler):
    """
    1a. The user goes to /uploads/new to upload a file, csv or xls
    1b. They POST this to /uploads/create
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

    def new(self, *args):
        pass

    def create(self, *args):
        self.format = 'json'

        files = self.request.params.get('files[]', None)
        print files

        # fdst = open(os.path.join(tmpdir, os.path.basename(files.filename)), 'wb')
        # shutil.copyfileobj(f.file, fdst)

            # walk in import directory to import all image files
        results = [{"success": "questionable"}]
        # result = dict(
        #     name=files.filename,
        #     size=get_size(files.file),
        #     delete_type="DELETE",
        #     url=self.request.static_path(settings['photos_dir']+'/orig/' + uri),
        #     thumbnail_url=self.request.static_path(['photos_dir']+'/scaled/' + uri),
        #     delete_url=self.request.route_path('photos_delete', _query=[('uri', uri)]))
        # done.append(result)

        return results
