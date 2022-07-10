import json


class Colour():
    def __init__(self, colour, rgbValue,  colourClass=[], tags=[]):
        self.__colour = colour
        self.__rgbValue = rgbValue
        self.__tags = tags
        self.__classification = colourClass

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #                       sort_keys=True, indent=4)


        
    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, colourClass):
        self.__tags = colourClass 
    
    @property
    def classification(self):
        return self.__classification

    @classification.setter
    def classification(self, colourClass):
        self.__classification = colourClass    
        
    @property
    def colour(self):
        return self.__colour

    @colour.setter
    def colour(self, colour):
        self.__colour = colour
        
    @property
    def rgbValue(self):
        return self.__rgbValue

    @rgbValue.setter
    def rgbValue(self, rgbValue):
        self.__rgbValue = rgbValue
        
    def __str__(self):
        return f'{self.colour} : {self.rgbValue}'

    def __repr__(self):
        return f'colour(colour={self.colour}, rgbValue={self.rgbValue}, tags=[{",".join([(str(item)) for item in self.tags])}])'
    