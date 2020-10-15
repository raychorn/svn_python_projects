import UserList

class SeqentialList(UserList.UserList):
    def next(self):
        try:
            return self.__cycler__.next()
        except AttributeError:
	    def iterate():
		for item in self:
		    yield item
		yield None
            self.__cycler__ = iterate()
            return self.next()
	except StopIteration:
	    return None
