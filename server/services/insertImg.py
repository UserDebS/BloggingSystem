import os
import base64
class InsertImage:
    def __init__(self) -> None:
        pass
    def insertImage(self, data : dict[str, any]) -> dict[str, any]:
        for key in data.keys():
            if(isinstance(data.get(key), dict)):
                data.update({key : self.insertImage(data.get(key))})
            elif(key == 'image' and (not str(data.get('image')).startswith('data:/image'))):
                imageData = self.__imageToBase64(data.get('image'))
                data.update({'image' : imageData})
            elif(isinstance(data.get(key), list)):
                data.update({key : self.__handleList(data.get(key))})
        return data
    
    def __handleList(self, data : list[any]) -> list[any]:
        for i in data:
            if(isinstance(i, dict)):
                i = self.insertImage(i)
            elif(isinstance(i, list)):
                i = self.__handleList(i)
        return data
    
    def __imageToBase64(self, imgName : str) -> str:
        parentDir = os.path.dirname(os.path.dirname(__file__))
        if(parentDir.endswith('server')):
            imgPath = '\\'.join([parentDir, f'storage\\{imgName}'])
            if(os.path.exists(imgPath)):
                with open(imgPath, 'rb') as img:
                    return f'data:image/{imgName.split(".")[-1]};base64,{base64.b64encode(img.read()).decode("utf-8")}'
        return imgName

if __name__ == '__main__':
    pass