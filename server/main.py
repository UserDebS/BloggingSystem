import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from recommend import Recommend
from datatypes import UserData, ContentWithText, Profile, ContentScreenData, ContentTitle
from database import Database

app = FastAPI()
db = Database()
recom = Recommend()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allows only the origins specified
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including POST, OPTIONS
    allow_headers=["Access-Control-Allow-Origin", 'Set-Cookie', 'Accept'],  # Allows all headers
)


@app.get('/') #auth by token will be used
async def landing_root(request : Request, response : Response): #Cookie Management route
    try:
        if(request.cookies.get('blog_auth') != None): #If Cookie is already present
            dbRes = db.authByToken(request.cookies.get('blog_auth'))
            if(dbRes.get('status') == 204): #Exists in Database
                response.set_cookie('blog_auth', dbRes.get('token'), max_age=15 * 24 * 3600 * 1000)
                return {
                    'status' : 200
                }
        raise HTTPException(status_code=404, detail='Token does not exist')
    except:
        raise HTTPException(status_code=404, detail='Token does not exist')

@app.post('/signup') #no auth. Only user registration
async def signUp(user : UserData, response : Response):
    try:
        dbRes = db.signup({
            'username' : user.username,
            'password' : user.password,
            'description' : user.description
        })
        if(dbRes.get('status') == 201):
            response.set_cookie('blog_auth', dbRes.get('token'), max_age=15 * 24 * 3600 * 1000)
            return {
                'status' : 201,
            }
        
        raise HTTPException(status_code=409, detail='User already exists')
    except:
        raise HTTPException(status_code=409, detail='User already exists')

@app.post('/login') #auth using username and password
async def logIn(user : UserData, response : Response):
    try:
        dbRes = db.auth({
            'username' : user.username,
            'password' : user.password
        })
        if(dbRes.get('status') == 204):
            response.set_cookie('blog_auth', dbRes.get('token'), max_age=15 * 24 * 3600 * 1000)
            return {
                'status' : 200
            }

        raise HTTPException(status_code=404, detail='User does not exist')
    except:
        raise HTTPException(status_code=404, detail='User does not exist')

@app.post('/upload') # token will be used for this purpose
async def upload(contentWithText : ContentWithText, request : Request) -> dict[str, int]:
    return db.uploadBlog(token=request.cookies.get('blog_auth'), contentWithText=contentWithText)

@app.get('/blogs/')
async def getBlogs(offset : int = 0) -> list[ContentTitle]:
    return db.fetchBlogs(offset=offset)

@app.get('/{username}/')
async def getChannel(username : str, offset: int = 0) -> Profile:
    profile =  db.fetchChannel(username, offset)
    if(profile == None):
        return HTTPException(status_code=404, detail='Channel Not Found')
    return profile

@app.get('/blogs/{blogId}/')
async def getBlogByID(blogId : int, offset : int = 0) -> ContentScreenData:
    contentScreenData : ContentScreenData = db.fetchBlogById(blogId, offset=offset)
    if(contentScreenData == None):
        raise HTTPException(status_code=404, detail='Blog not found')
    return contentScreenData

@app.get('/blogs/')
async def getBlogBySearch(search : str, offset : int = 0) -> list[ContentTitle]:
    return db.fetchBlogBySearch(search, offset)


if __name__ == '__main__':
    uvicorn.run(app=app, port=5500)