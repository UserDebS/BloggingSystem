from os import getenv
from dotenv import load_dotenv
from supabase import create_client
from services.encryption import strGen, encryption
from datatypes import ContentTitle, Content, ContentWithText, ContentScreenData, Profile
from recommend import Recommend
from services.recommendMapping import recommendMapping
from services.extractImg import ImageExtraction
from services.insertImg import InsertImage
from services.typeConvertor import dictToList
from datetime import datetime

load_dotenv()

recommSystem = Recommend()
imgExtract = ImageExtraction()
imgInsert = InsertImage()

class Database:
    def __init__(self) -> None:
        self.__instance = create_client(supabase_key=getenv('SUPABASE_KEY'), supabase_url=getenv('SUPABASE_URL'))

    def select(self, table : str, query : str = '') -> list[str, any]:
        return self.__instance.table(table).select(query).execute().data
    
    def signup(self, data : dict[str, str]) -> dict[str, any]:
        try:
            salt = strGen(20)
            newtoken = strGen(30)
            username = data.get('username')
            password = data.get('password')
            description = data.get('description')
            password = encryption(encryption(salt) + encryption(password))
            self.__instance.table('users').insert({
                'username' : username,
                'password' : password,
                'description' : description,
                'salt' : salt,
                'token' : encryption(newtoken)
            }).execute()
            return {
                'status' : 201,
                'token' : newtoken
            }
        except:
            return {
                'status' : 409
            }
        
    def auth(self, data : dict[str, str]) -> dict[str, any]:
        try: 
            response = self.__instance.table('users').select('password, salt').eq('username', data['username']).single().execute().data
            password = encryption(encryption(response['salt']) + encryption(data['password']))
            if(password == response['password']):
                salt = strGen(20)
                newtoken = strGen(30)
                password = encryption(encryption(salt) + encryption(data['password']))
                self.__instance.table('users').update({
                    'salt' : salt,
                    'password' : password,
                    'token' : encryption(newtoken)
                }).eq('username', data['username']).execute()
                return {
                    'status' : 204,
                    'token' : newtoken
                }
            else:
                return {
                    'status' : 404
                }
        except:
            return {
                'status' : 404
            }
        
    def authByToken(self, token : str) -> dict[str, any]:
        try: 
            response = self.__instance.table('users').select('id').eq('token', encryption(token)).single().execute().data
            newtoken = strGen(30)
            self.__instance.table('users').update({
                'token' : encryption(newtoken)
            }).eq('id', response['id']).execute()
            return {
                'status' : 204,
                'token' : newtoken
            }
        except:
            return {
                'status' : 404
            }
        
    def uploadBlog(self, token : str, contentWithText : ContentWithText) -> dict[str, int]:
        try: 
            blog_tags : dict[str, bool] = recommendMapping(recommSystem.compareBoolList(recommSystem.compareHashTags(contentWithText.quillData.tags), recommSystem.compareContent(contentWithText.text)))
            contentWithText.quillData.content = imgExtract.extractImage(contentWithText.quillData.content)
            self.__instance.rpc('content_uploader', {
                'input_token' : encryption(token),
                'input_title' : contentWithText.quillData.title,
                'input_content' : contentWithText.quillData.content,
                'blog_tags' : blog_tags
            }).execute()
            return {
                'status' : 201
            }
        except Exception as e:
            return {
                'err' : e,
                'status' : 422
            }

    def fetchBlogs(self, offset : int = 0) -> list[ContentTitle]:
        try:
            return list(map(lambda blog: {
                'title' : blog['title'],
                'username' : blog['username'],
                'tags' : list(blog['tags'].keys()),
                'self_url' : blog['self_url']
            }, self.__instance.table('get_blogs').select('*').offset(offset).execute().data))
        except:
            return []

    def fetchBlogById(self, blogId : int, offset : int) -> ContentScreenData | None:
        try:
            data : dict[str, any] = self.__instance.table('blogs').select('blog_title, blog_content, tag_list').eq('blog_id', blogId).single().execute().data
            return ContentScreenData(**{
                'content' : Content(**{
                    'title' : data.get('blog_title'),
                    'content' : imgInsert.insertImage(data.get('blog_content')),
                    'tags' : list(data['tag_list'].keys())
                }),
                'related_blogs' : list(map(dictToList, self.__instance.rpc('get_matching_blogs_formatted', {
                    'blog_input_id' : blogId,
                    'offst' : offset
                }).execute().data))})
        except Exception as e:
            print(e)
            return None

    def fetchBlogBySearch(self, search : str, offset : int = 0) -> list[ContentTitle]:
        try:
            referenceList = recommSystem.compareBoolList(recommSystem.compareContent(search), recommSystem.compareHashTags(search.split(',')))
            return list(map(lambda blog: {
                'title' : blog['title'],
                'username' : blog['username'],
                'tags' : list(blog['tags'].keys()),
                'self_url' : blog['self_url']
            }, self.__instance.rpc('get_blogs_from_bool_arr_formatted', {
                'b_arr' : referenceList,
                'offst' : offset
            }).execute().data))
        except:
            return []

    def fetchChannel(self, username : int, offset : int = 0) -> Profile | None:
        try:
            result = self.__instance.table('get_channel').select('*').eq('username', username).offset(offset).execute().data

            return Profile(**{
                'username' : username,
                'description' : result[0]['description'],
                'joined_at' : datetime.fromisoformat(result[0]['created_at']).strftime('%d-%m-%Y'),
                'blogs' : list(map(dictToList, result))
            })
        except Exception as e:
            print(e)
            return None

if __name__ == '__main__':
    db = Database()
    print(db.fetchChannel('admin'))