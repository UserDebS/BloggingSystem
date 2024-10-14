import os
import base64

if __name__ == '__main__':
    curDir = os.path.dirname(__file__)
    parentDir = os.path.dirname(curDir)
    if(parentDir.endswith('server')):
        storageDir = '\\'.join([parentDir, 'storage'])
        data = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABcElEQVR42mJ0gG6SgBQAE4A7D4IQQiIAEZMmlgHgZNAH0F4AIAw8C8wIY3mgAwcMGE6EIgoEEAwgEgAABDAAAABAAAAAICUAAeEAAAAAElFTkSuQmCC'
        missing = len(data) % 4
        data += '=' * (4 - missing)
        with open('\\'.join([storageDir, f'output.png']), 'wb') as f:
                f.write(base64.b64decode(data))
            
    