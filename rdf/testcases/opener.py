import os.path
from urllib.request import OpenerDirector, BaseHandler, Request, URLError


class URItoFileHandler(BaseHandler):
    def __init__(self, path_map):
        super().__init__()
        self.path_map = path_map

    def default_open(self, req):
        if isinstance(req, Request):
            url = req.full_url
        else:
            url = req
        for prefix, head in self.path_map.items():
            if url.startswith(prefix):
                tail = url[len(prefix):]
                return open(os.path.join(head, tail))
        raise URLError(url)

class URItoFileOpener(OpenerDirector):
    def __init__(self, path_map=None):
        super().__init__()
        if path_map is not None:
            self.add_handler(URItoFileHandler(path_map))

