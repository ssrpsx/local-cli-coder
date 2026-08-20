from local_coder.__main__ import multi


def test_multi():
    assert multi(2, 3) == 6
    assert multi(1, 8) == 8
    assert multi(11, 6) == 66
    assert multi(55, 3) == 165
