def eq_(a, b, msg=None):
    assert a == b, msg or '%s != %s' % (a, b)
