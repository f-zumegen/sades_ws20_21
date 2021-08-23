
class Observable():
    def __init__(self):
        self._observers = []

    def attach( self, observer ):
        self._observers.append( observer )        

    def detach( self, observer ):
        self._observers.remove( observer ) 

    def notify( self, msg ):
        for observer in self._observers:
            # print("Observer:", observer)
            observer.update( msg )


class Observer():
    def update(self, msg): raise NotImplementedError


