import json


class Smell():
    def __init__(self, smell, description, smellClass=[], tags=[]):
        self.__smell = smell
        self.__description = description
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
  
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description
        
                
        
    def __str__(self):
        return f'{self.smell} : {self.description}'

    def __repr__(self):
        return f'smell(smell={self.smell}, description={self.description}, tags=[{",".join([(str(item)) for item in self.tags])}])'
    