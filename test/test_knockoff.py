from sklearn.utils.estimator_checks import check_estimator

from knock_off import KnockOff


def test_estimator_KnockOff():
    check_estimator(KnockOff())
