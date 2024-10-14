import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from recommend import Recommend
from datatypes import UserData, ContentWithText, ContentTitle
from database import Database

from services.recommendMapping import recommendMapping

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
    if(request.cookies.get('blog_auth') != None): #If Cookie is already present
        dbRes = db.authByToken(request.cookies.get('blog_auth'))
        if(dbRes.get('status') == 204): #Exists in Database
            response.set_cookie('blog_auth', dbRes.get('token'), max_age=15 * 24 * 3600 * 1000)
            return {
                'status' : 200
            }
    return {
        'status' : 404
    }

@app.post('/signup') #no auth. Only user registration
async def signUp(user : UserData, response : Response):
    dbRes = db.signup({
        'username' : user.username,
        'password' : user.password
    })
    if(dbRes.get('status') == 201):
        response.set_cookie('blog_auth', dbRes.get('token'), max_age=15 * 24 * 3600 * 1000)
        return {
            'status' : 200,
        }
    return {
        'status' : 404
    }

@app.post('/login') #auth using username and password
async def logIn(user : UserData, response : Response):
    dbRes = db.auth({
        'username' : user.username,
        'password' : user.password
    })
    if(dbRes.get('status') == 204):
        response.set_cookie('blog_auth', dbRes.get('token'), max_age=15 * 24 * 3600 * 1000)
        return {
            'status' : 200
        }
    return {
        'status' : 404
    }

@app.post('/upload') # token will be used for this purpose
async def upload(contentWithText : ContentWithText, request : Request) -> dict[str, int]:
    return db.uploadBlog(token=request.cookies.get('blog_auth'), contentWithText=contentWithText)

@app.get('/blogs/')
async def getBlogs(offset : int = 0) -> list[ContentTitle]:
    return db.fetchBlogs(offset=offset)

@app.get('/{username}/')
async def getChannel(username : str, offset: int) :#-> Profile:
    return {
        'channel-name' : username
    }

@app.get('/blogs/{blogId}/')
async def getBlogByID(blogId : int, offset : int) :#-> ContentScreenData:
    return {
        'blog-id' : blogId
    }

@app.get('/blogs/')
async def getBlogBySearch(search : str, offset : int) -> list[ContentTitle]:
    return {
        'search-param' : search
    }

@app.get('/')
async def getKeywordsFromText(keywords : str) -> list[str]:
    return recommendMapping(recom.compareContent(keywords), _type='list')

if __name__ == '__main__':
    uvicorn.run(app=app, port=5500)