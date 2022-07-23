import json


class ColourDescriptor():
    def __init__(self, descriptor, description,descriptorClass=[], tags=[]):
        self.__descriptor = descriptor
        self.__description = description
        self.__tags = tags
        self.__classification = descriptorClass

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #                       sort_keys=True, indent=4)

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description 

        
    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, descriptorClass):
        self.__tags = descriptorClass 
    
    @property
    def classification(self):
        return self.__classification

    @classification.setter
    def classification(self, descriptorClass):
        self.__classification = descriptorClass    
        
    @property
    def descriptor(self):
        return self.__descriptor

    @descriptor.setter
    def descriptor(self, descriptor):
        self.__descriptor = descriptor
        

        
    def __str__(self):
        return f'{self.descriptor} : {self.rgbValue}'

    def __repr__(self):
        return f'descriptor(descriptor={self.descriptor}, description={self.description}, tags=[{",".join([(str(item)) for item in self.tags])}])'
    