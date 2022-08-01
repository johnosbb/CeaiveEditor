import json


class Smell():
    def __init__(self, smell,  smellClass=[], tags=[]):
        self.__smell = smell
        self.__tags = tags
        self.__classification = smellClass

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #                       sort_keys=True, indent=4)


        
    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, smellClass):
        self.__tags = smellClass 
    
    @property
    def classification(self):
        return self.__classification

    @classification.setter
    def classification(self, smellClass):
        self.__classification = smellClass    
        
    @property
    def smell(self):
        return self.__smell

    @smell.setter
    def smell(self, smell):
        self.__smell = smell
        
        
    def __str__(self):
        return f'{self.smell} : {self.rgbValue}'

    def __repr__(self):
        return f'smell(smell={self.smell},  tags=[{",".join([(str(item)) for item in self.tags])}])'
    