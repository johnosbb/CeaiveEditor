import json


class Sound():
    def __init__(self, sound, rgbValue,  soundClass=[], tags=[]):
        self.__sound = sound
        self.__rgbValue = rgbValue
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
    def rgbValue(self):
        return self.__rgbValue

    @rgbValue.setter
    def rgbValue(self, rgbValue):
        self.__rgbValue = rgbValue
        
    def __str__(self):
        return f'{self.sound} : {self.rgbValue}'

    def __repr__(self):
        return f'sound(sound={self.sound}, rgbValue={self.rgbValue}, tags=[{",".join([(str(item)) for item in self.tags])}])'
    