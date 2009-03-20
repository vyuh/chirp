import hashlib, os, shutil, tempfile, time, urllib

class DiskCacheFetcher(object):
    """
    Mechanism for caching urllib.urlopen() calls to a temporary file
    source: http://developer.yahoo.com/python/python-caching.html
    """

    def __init__(self):
        self.cache_dir = tempfile.mkdtemp()

    def fetch(self, url, max_age=0):
        # Use MD5 hash of the URL as the filename
        filename = hashlib.md5(url).hexdigest()
        filepath = os.path.join(self.cache_dir, filename)
        if os.path.exists(filepath):
            if int(time.time()) - os.path.getmtime(filepath) < max_age:
                return open(filepath).read()

        # Retrieve over HTTP and cache, using rename to avoid collisions
        data = urllib.urlopen(url).read()
        fd, temppath = tempfile.mkstemp()
        fp = os.fdopen(fd, 'w')
        fp.write(data)
        fp.close()
        os.rename(temppath, filepath)
 
        return data 

    def cleanup(self):
        shutil.rmtree(self.cache_dir)

