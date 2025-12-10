from abc import ABC, abstractmethod

class VisualizerBase(ABC):

    @abstractmethod
    def redraw(self, simulation):
        pass