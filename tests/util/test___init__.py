import banana_inspector.util as ut


def test_str2sec():
    assert ut.str2sec('2018') - 1514764800.0 == 0
    assert ut.str2sec('2018-01') - 1514764800.0 == 0
    assert ut.str2sec('2018-01-01') - 1514764800.0 == 0
    assert ut.str2sec('2018-01-01 00') - 1514764800.0 == 0
    assert ut.str2sec('2018/01/01 00') - 1514764800.0 == 0
    assert ut.str2sec('2018/01/01T00') - 1514764800.0 == 0

