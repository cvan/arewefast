def get_resource_type(ct, url):
    # Strip everything after the hash and the querystring (if present).
    ext = (url or '').rsplit('#', 1)[0].rsplit('?', 1)[0].lower()

    ct = (ct or '').lower()

    if ct.startswith('text/css'):
        return 'css'

    if 'javascript' in ct:
        return 'js'

    if '/json' in ct:
        return 'json'  # XHR?

    if '/xml' in ct or ext.endswith('.xml'):
        return 'xml'  # XHR?

    if 'flash' in ct:
        return 'flash'

    # TODO: Determine if an img is inline by requesting all the CSS
    # (with the same request headers) and getting a hash of all the images.

    # TODO: But then we need to differentiate between those and <img>s?
    # And the only way is to get the post-JS DOM.

    if ct.startswith('image/'):
        return 'image'

    if ct.startswith('audio/'):
        return 'audio'

    if ct.startswith('video/'):
        return 'video'

    # TODO: Figure out how to count `image/svg+xml` as font when used as such.

    if (ct.startswith(('application/font-', 'application/vnd.ms-fontobject',
                       'application/x-font-', 'font/'))):
        return 'font'

    if ext.endswith('.js'):
        return 'js'

    if ext.endswith('.css'):
        return 'css'

    # TODO: Include '.svg'?
    if ext.endswith(('.eot', '.otf', '.ttf', '.woff')):
        return 'font'

    if ext.endswith('.swf'):
        return 'flash'

    if ext.endswith(('.bmp', '.fpx', '.gif', '.j2c', '.j2k', '.jfif', '.jif',
                     '.jp2', '.jpe', '.jpeg', '.jpg', '.jpx', '.pcd', '.png',
                     '.tif', '.tiff', '.webp', '.woff')):
        return 'image'

    if ext.endswith(('.flac', '.m4a', '.mid', '.mp3', '.mpa', '.ra', '.ogg',
                     '.opus', '.wav', '.weba', 'wma')):
        return 'audio'

    if ext.endswith(('.avi', '.flv', '.h264', '.mov', '.mp4', '.mp4v', '.mpg',
                     '.rm', '.webm', '.wmv')):
        return 'video'

    if (ct.startswith(('text/html', 'text/plain') or
        ext.startswith(('.htm', '.html', '.jsp', '.php', '.txt', '.markdown',
                       '.md')))):
        return 'doc'

    return 'other'
