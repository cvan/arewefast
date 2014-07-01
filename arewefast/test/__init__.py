def eq_(a, b, msg=None):
    assert a == b, msg or '%r != %r' % (a, b)
