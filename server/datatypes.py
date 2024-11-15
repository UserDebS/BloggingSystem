from pydantic import BaseModel

class UserData(BaseModel):
    username : str
    password : str
    description : str = 'N/A'

class Content(BaseModel):
    title : str
    content : dict[str, list[dict[str, str | dict[str, str | int | bool]]]]
    tags : list[str] # will be used for searching purpose

class ContentWithText(BaseModel):
    quillData : Content
    text : str

class ContentTitle(BaseModel): # Video box titles just like youtube
    title : str
    username : str
    tags : list[str]
    self_url : str

class ContentScreenData(BaseModel):
    content : Content
    related_blogs : list[ContentTitle] # recommended similar blogs to current blog

class Profile(BaseModel): # the profile page itself.
    username : str
    description : str
    joined_at : str
    blogs : list[ContentTitle]