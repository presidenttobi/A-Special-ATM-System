class InvalidPinError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class AccountNotFoundError(Exception):
    pass


class NegativeAmountError(Exception):
    pass


class DuplicateAccountError(Exception):
    pass


class DuplicatePinError(Exception):
    pass


class AccountLockedError(Exception):
    pass


class SameAccountError(Exception):
    pass
