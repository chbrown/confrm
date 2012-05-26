class Site(object):
    name = None

    def __json__(self):
        # (name=self.name)
        return self.__dict__

site = Site()
