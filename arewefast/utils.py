def get_resource_type(ct, url):
    # Strip everything after the hash and the querystring (if present).
    fn = (url or '').rsplit('#', 1)[0].rsplit('?', 1)[0].lower()

    # Strip everything after a semicolon (e.g., `; charset=utf-8`).
    ct = (ct or '').rsplit(';', 1)[0].lower()

    if ct.startswith('text/css') or fn.endswith('.css'):
        return 'css'

    if 'javascript' in ct or fn.endswith('.js'):
        return 'js'

    if ('/json' in ct or '+json' in ct or '-json' in ct or
        fn.endswith('.json')):
        return 'json'  # XHR?

    if '/xml' in ct or fn.endswith('.xml'):
        return 'xml'  # XHR?

    if 'flash' in ct:
        return 'flash'

    # TODO: Determine if an img is inline by requesting all the CSS
    # (with the same request headers) and getting a hash of all the images.

    # TODO: But then we need to differentiate between those and <img>s?
    # And the only way is to get the post-JS DOM.

    if (ct.startswith('image/') or
        fn.endswith(('.bmp', '.fpx', '.gif', '.j2c', '.j2k', '.jfif', '.jif',
                     '.jp2', '.jpe', '.jpeg', '.jpg', '.jpx', '.pcd', '.png',
                     '.tif', '.tiff', '.webp'))):
        return 'image'

    if (ct.startswith('audio/') or
        fn.endswith(('.flac', '.m4a', '.mid', '.mp3', '.mpa', '.ra', '.ogg',
                     '.opus', '.wav', '.weba', 'wma'))):
        return 'audio'

    if (ct.startswith('video/') or
        fn.endswith(('.avi', '.flv', '.h264', '.mov', '.mp4', '.mp4v', '.mpg',
                     '.rm', '.webm', '.wmv'))):
        return 'video'

    # TODO: Figure out how to count `image/svg+xml` as font when used as such.
    # TODO: Include '.svg' extension (since could be used for image)?
    if (ct.startswith(('application/font-', 'application/vnd.ms-fontobject',
                       'application/x-font-', 'font/')) or
        fn.endswith(('.eot', '.otf', '.ttf', '.woff'))):
        return 'font'

    # Don't count `.flv` since counted as a video.
    if ct.endswith('-flash') or fn.endswith('.swf'):
        return 'flash'

    # Documents are flat text, not binaries such as `.doc` and `.xls`.
    if (ct.startswith(('text/html', 'text/plain')) or
        fn.endswith(('.htm', '.html', '.jsp', '.php', '.txt', '.markdown',
                       '.md'))):
        return 'doc'

    return 'other'
