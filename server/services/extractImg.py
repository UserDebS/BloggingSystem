''' 
It will be recursive algorithm which will recursively search for image base64 data and replace them with unique string names generated at very first of each call.
'''
from .encryption import strGen
import base64
import os

class ImageExtraction:
    def __init__(self) -> None:
        self.currentImageList : dict[str, str] = {}
        self.currentGeneratedImageName : str = ''
        self.iterator : int = 0

    def extractImage(self, data : dict[str, any]) -> dict[str, any]:
        self.currentGeneratedImageName = strGen(20);
        self.iterator = 0
        data : dict[str, any] = self.__extractImage(data)
        self.__generateImage()
        return data
    
    def __generateImage(self) -> None:
        parentDir = os.path.dirname(os.path.dirname(__file__))
        if(parentDir.endswith('server')):
            storageDir = '\\'.join([parentDir, 'storage'])
            for imgName in self.currentImageList.keys():
                with open(f'{storageDir}\\{imgName}', 'wb') as img:
                    img.write(base64.b64decode(self.currentImageList.get(imgName)))

    def __getImageType(self, img : str, data : str) -> dict[str, str]: # returns a key value pair of imagename with extension and pure base64 value
        key : str = f"{img}.{data.split(';')[0].split('/')[-1]}"
        value : str = data.split(',')[-1].lstrip().rstrip()
        value += '=' * (4 - (len(value) % 4))
        return {key : value}

    def __imageNameGen(self) -> str:
        imageName : str = self.currentGeneratedImageName + f'{self.iterator}'
        self.iterator += 1
        return imageName

    def __extractImage(self, data : dict[str, any]) -> dict[str, any]:
        for key in data.keys():
            if(isinstance(data.get(key), dict)):
                data.update({key : self.__extractImage(data.get(key))})
            elif(key == 'image'):
                if(str(data.get('image')).startswith('data:image/')):
                    imageData = self.__getImageType(self.__imageNameGen(), data.get('image'))
                    self.currentImageList.update(imageData)
                    data.update({'image' : list(imageData.keys())[0]})
            elif(isinstance(data.get(key), list)):
                data.update({key : self.__handleList(data.get(key))})
        return data
    
    def __handleList(self, data : list[any]) -> list[any]:
        for i in data:
            if(isinstance(i, dict)):
                i = self.__extractImage(i)
            elif(isinstance(i, list)):
                i = self.__handleList(i)
        return data

if __name__ == '__main__':
    i = ImageExtraction()
    with open('testImage.txt', 'r') as f:
        a = f.read()
        print(i.extractImage({
            'ops': [
                { 'insert': 'This is a sample blog post with various types of content.\n' },
                { 'insert': 'Section Title', 'attributes': { 'bold': True, 'header': 2 } },
                { 'insert': '\nHere is some regular paragraph text with an image:\n' },
                { 'insert': { 'image': f'data:image/png;base64,{a}' } },
                { 'insert': '\nNow let\'s add a list of items:\n' },
                { 'insert': 'First item', 'attributes': { 'bold': True } },
                { 'insert': '\n' },
                { 'insert': 'Second item' },
                { 'insert': '\n', 'attributes': { 'list': 'bullet' } },
                { 'insert': 'Third item', 'attributes': { 'list': 'bullet' } },
                { 'insert': '\nLet\'s add another image here:\n' },
                { 'insert': { 'image': f'data:image/png;base64,{a}' } },
                { 'insert': '\nFinally, some italic text to conclude.\n', 'attributes': { 'italic': True } }
            ]
            }))