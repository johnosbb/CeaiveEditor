import json


class Sound():
    def __init__(self, sound, description,  soundClass=[], tags=[]):
        self.__sound = sound
        self.__description = description
        self.__tags = tags
        self.__classification = soundClass

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #                       sort_keys=True, indent=4)


        
    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, soundClass):
        self.__tags = soundClass 
    
    @property
    def classification(self):
        return self.__classification

    @classification.setter
    def classification(self, soundClass):
        self.__classification = soundClass    
        
    @property
    def sound(self):
        return self.__sound

    @sound.setter
    def sound(self, sound):
        self.__sound = sound
        
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description
        
    def __str__(self):
        return f'{self.sound} : {self.description}'

    def __repr__(self):
        return f'sound(sound={self.sound}, description={self.description}, tags=[{",".join([(str(item)) for item in self.tags])}])'
    