from abc import ABC, abstractproperty


class BaseError(ABC):

    @abstractproperty
    def NOT_EXISTS(self):
        '''Ошибка несуществования'''

    @abstractproperty
    def ALREADY_EXISTS(self):
        '''Объект уже существует'''