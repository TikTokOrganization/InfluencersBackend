import abc

class VideoGetter(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getCategories') and \
            callable(subclass.getCategories) and \
            hasattr(subclass, 'getShortsOfCategory') and \
            callable(subclass.getShortsOfCategory))