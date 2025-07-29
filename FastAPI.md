## FASTAPI

官网：https://fastapi.tiangolo.com/tutorial/

#### 创建python虚拟环境与FastAPI安装

##### 1. 创建虚拟环境

```bash
conda create -n 虚拟环境名称  python=3.10 -y
# 添加清华源通道
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
conda activate 虚拟环境名称 
python -m venv 虚拟环境名称
虚拟环境名称\Scripts\activate
source 虚拟环境名称/bin/activate
```

##### 2.查看python版本

```bash
python --version
```

##### 3. 升级pip

```bash
pip install --upgrade pip
```

##### 5.pip下载包

```
pip echo 'fastapi==0.111.0' >requirements.txt
```

##### 6.检查

```
fastapi --version
```

#### 最简单的FastAPI应用程序与uvicorn

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"}
```

**启动**

```bash
uvicorn main:app \ #用于加载和运行你的应用程序的服务器 只支持http和websoket
--port 8080 \ #端口
--reload #热加载，只能用于开发环境
```

swagger UI:http://127.0.0.1:8000/docs

ReDoc openapi:http://127.0.0.1:8000/redoc

#### http

```python
from fastapi import FastAPI,Request

app = FastAPI()
@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/resources/path/{file}")
@app.post("/resources/path/{file}")
@app.put("/resources/path/{file}")
@app.delete("/resources/path/{file}")
async def http_url(*,request: Request,key1,key2):
    response = {
        "协议名称":request.url.scheme, # 获取URL的协议
        "主机名称":request.url.hostname,# 获取url的主机名
        "端口":request.url.port,# 获取url的端口
        "资源路径":request.url.path, # 获取url的资源路径
        "参数":request.url.query, # 获取url的参数（键值对）
        "key1的值":key1,
        "key2的值":key2,
        "请求头部":request.headers,
        "请求体":await request.body(),
    }
    return response
```

#### cookie

```python
@app.get("show_me_the_cookie")
async def get_the_cookie(response:Response):
    # cookie可以是客户端自己设置的，也可以服务器返回给客户端的
    # 过期时间15秒
    response.set_cookie(key="fake_session_cookie",value="20250727001",expires=15)
    return {"响应信息":"我们有cookie了，还在cookie里增加了一个假的cookie_id"}
```

#### 运行状态检查(Uptime Kuma)

```python
@app.get("/server-status",include_in_schema=False) # swagger UI 隐藏起来
async def serverStatus(response: Response,token: str | None=None):
    if token == "Tai":
        data = {
            "运行状态":"正常运行"
        }
        return data
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":"Not Found"}
```

#### 返回文件

```python 
@app.get("/favicon.ico",include_in_schema=False)
async def favicon():
    return FileResponse("tmp/favicon.ico")
```

#### 静态文件

```python
app.mount("/sub", StaticFiles(directory="static"), name="static")
# 使用StaticFiles从目录中自动提供静态文件
# 挂载表示特定路径添加一个完全“独立”应用，然后负责处理所有子路径
```

#### 子应用

```python
app = FastAPI()
son_app = FastAPI()

@son_app.get("/")
async def root():
    return {"data":"我是子应用，独立存在的！"}
@son_app.get("/info")
async def info():
    return {"data":"这是子应用son返回来的信息！"}

son_app.mount("/grand_son", grand_son_app, name="grand_son")
app.mount("/son",son_app,name="son")
```

#### 模板功能

```python
app = FastAPI()

app.mount("/sub", StaticFiles(directory="static"), name="static")

@app.get("/post-v1")
async def post_html_v1():
    data = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FastAPI开发与部署</title>
    <link href="http://127.0.0.1:8080/sub/css/main.css" rel="stylesheet">
</head>
<body>
    <h1>这是post页面</h1>
    <article>
        <header>这是一篇文章</header>
        <section>这篇文章的具体内容部分，标题和文章主体部分都是可变的。</section>
    </article>
    <h1>这里可以访问video页面</h1>
    <article>
        <section>
            <a href="http://127.0.0.1:8080/videos/1">查看1个视频</a>
        </section>
    </article>
</body>
</html>
    """
    return HTMLResponse(content=data)

@app.get("/post-v2")
async def post_html_v2():
    name = "FastAPI开发与部署"
    id = 1
    title = "这是一篇文章"
    body = "这篇文章的具体内容部分，标题和文章主体部分都是可变的。"
    data = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{name}</title>
    <link href="http://127.0.0.1:8080/sub/css/main.css" rel="stylesheet">
</head>
<body>
    <h1>这是post页面</h1>
    <article>
        <header>{title}</header>
        <section>{body}</section>
    </article>
    <h1>这里可以访问video页面</h1>
    <article>
        <section>
            <a href="http://127.0.0.1:8080/videos/1">查看{id}个视频</a>
        </section>
    </article>
</body>
</html>
    """
    return HTMLResponse(content=data)

def html_maker(*,content:dict,request:Request):
    name = content.get("name")
    id = content.get("id")
    title = content.get("title")
    body = content.get("body")

    data = f"""
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{name}</title>
        <link href="{request.url_for('statics',path='/css/main.css')}" rel="stylesheet">
    </head>
    <body>
        <h1>这是post页面</h1>
        <article>
            <header>{title}</header>
            <section>{body}</section>
        </article>
        <h1>这里可以访问video页面</h1>
        <article>
            <section>
                <a href="{request.url_for('videos_function',video_id=id)}">查看{id}个视频</a>
            </section>
        </article>
    </body>
    </html>
        """
    return HTMLResponse(content=content)
@app.get("/post-v3")
async def post_html_v3(request: Request):
    data = {
        "name": "FastAPI开发与部署",
        "id": 1,
        "title": "这是一篇文章",
        "body": "这篇文章的具体内容部分，标题和文章主体部分都是可变的。"
    }
    return html_maker(content=data,request=request)

```

#### Jinj2

**post.html**

```html
<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{site.name}}</title>
        <link href="{request.url_for('statics',path='/css/main.css')}" rel="stylesheet">
    </head>
    <body>
        <h1>这是post页面</h1>
        <article>
            <header>{{page.title}}</header>
            <section>{{page.body}}</section>
        </article>
        <h1>这里可以访问video页面</h1>
        <article>
            <section>
                <a href="{request.url_for('videos_function',video_id=id)}">查看{{id}}个视频</a>
            </section>
        </article>
    </body>
    </html>
```

**head.html**

```html
<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{site.name}}</title>
```

**videos.html**

```html
{% include 'common/head.html'%}
<body>
    {% if id %}
    <h1>这是第{{id}}个视频</h1>
    <div>
        <video width="800" controls>
        	<source src="{{ url_for('play','video_id-id')}}" type="video/mp4">
        </video>
    </div>
    {% else %}
    <h1>没有视频存在</h1>
    {% endif %}
</body>
</html>
```

**main.py**

```python
templates = Jinja2Templates(directory="front_end/templates")

class Site(BaseModel):
    name: str = "FastAPI开发与部署"

page = {
    "title":"这是一篇文章",
    "body":"这篇文章的具体内容部分，标题和文章主体部分是可变的"
}

@app.get("/post")
async def post(request: Request):
    data = {
        "site": Site(),
        "page": page,
        "id": 1
    }
    return templates.TemplateResponse(name="post.html", context=data,request=request)

@app.get("/videos/{video_id}")
async def videos_function(request: Request,video_id:int):
    if video_id > 1 or video_id < 1:
        video_id = None
    data ={
        "site": Site(),
        "id": video_id
    }
    return templates.TemplateResponse(name="video.html", context=data,request=request)

@app.get("/file/{video_id}")
async def play(video_id):
    return FileResponse(f"front_end/resources/{video_id}.mp4")
```

#### 环境变量

**config.py**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # debug模式
    DEBUGE_MODE: bool = True
    # 静态目录
    STATIC_DIR: str = "static"
    STATIC_URL: str = "/sub"
    STATIC_NAME: str = "statics"
    # 模板目录
    TEMPLATE_DIR: str
    class Config:
        env_file = (".env",".env.prod") # 后面的会覆盖前面的
    
config = Settings()
```

**.env**

```python
# debug模式
DEBUGE_MODE=True
# 静态目录
STATIC_DIR="static"
STATIC_URL="/sub"
STATIC_NAME="statics"
```

****

#### FastAPI实现缓存

```python
from functools import lru_cache # 引入内建的 functools 包里的 lru缓存
@lru_cache(maxsize=1024)
def lru_test(change):
    print("如果显示本信息，就是还没有缓存")
    time.sleep(8)
    data = {
        "site": Site(),
        "page": page,
        "id": change
    }
    print("返回结果前，先睡8秒")
    return data

@app.get('/post/{change}')
async def post(request:Request,change:int):
    data = lru_test(change)
    print(lru_test.cache_info())
    return templates.TemplateResponse(name="post.html",context=data,request=request)
```

#### 路径和简易短链接服务

```python
class Site(BaseModel):
    name: str = "FastAPI开发与部署"

page = {
    "title":"这是一篇文章",
    "body":"这篇文章的具体内容部分，标题和文章主体部分是可变的"
}

@app.get("/post/1")
async def post(request: Request):
    data = {
        "site": Site(),
        "page": page,
        "id": 1
    }
    return templates.TemplateResponse(name="post.html", context=data,request=request)

# 独立变量
@app.get("/post/{path_1}/{path_2}")
async def post(request: Request,path_1: str,path_2: Annotated[str | None,Path(title="路径变量2")]):# 可选（str | None）
    data = {
        "site": Site(),
        "page": page,
        "id": 1,
        "path_1": path_1,
        "path_2": path_2
    }
    return templates.TemplateResponse(name="post.html", context=data,request=request)
@app.get("/{path_1}/2")
async def post(path_1: str |None = None):# 设置默认值为None
    data={
        "path_1":path_1
    }
    return data

class TypeName(str, Enum):
    blog: str = "blog"
    comment: str = "comment"
    page: str = "page"

# 预设值变量
@app.get("/type/{type_name}")
async def post(request: Request,type_name:TypeName = Path(title="模块变量",description="可以用的模块变量：blog comment page")):
    data = None
    if type_name == TypeName.blog:
        data = "blog模块"
    if type_name == TypeName.comment:
        data = "留言模块"
    if type_name == TypeName.page:
        data = "单页面模块"
    
    return {"module":data}

# 包含路径的变量
@app.get("/post/{file_path:path}")# 包含post后面全部的值
async def post(file_path: Path):
    return {"file_path": file_path}

@app.get("/videos/{video_id}")
async def videos_function(request: Request,video_id:int = Path(...,gt=0,lt=2,title="voice的id",description="它只能为1")): #必选项，>0 <2
    if video_id > 1 or video_id < 1:
        video_id = None
    data ={
        "site": Site(),
        "id": video_id
    }
    return templates.TemplateResponse(name="video.html", context=data,request=request)

```

```python
class PostItem(BaseModel):
    original_url: str

@app.post("/short/")
async def short_post(request:Request,post: PostItem):
    short_url = short_random(original_url=post.original_url)
    store_short_url(short_url, post.original_url)
    return {"short_url":short_url}

@app.get("/short/{short_url}")
async def short(short_key: str):
    url = get_url_by_key(short_key)
    # return {"original_url":url}
    return RedirectResponse(f"http://{url}")
def get_url_by_key(short_key):
    db = dbm.open(URL_DB,"c")
    url = db.get(short_key)
    db.close()
    return url

# 生成一个随机短链接
# 默认为8个字符长度
def short_random(*,original_url:str,length:int = 8):#`*`符号用于强制其后的参数必须以关键字参数的形式传递
    random_str = hashlib.md5(original_url.encode()).hexdigest()[:length]
    return random_str

# 通过dbm存储短链接
def store_short_url(short_url:str, original_url:str):
    db = dbm.open(URL_DB,"c")
    db[short_url] = original_url.encode("utf-8")
    db.close()
```

#### 文件上传

```python
@app.post("/upload_file",summary="上传文件")
async def upload_file(file: UploadFile):
    return {
        "file_name": file.filename,
        "content_type": file.content_type
    }

@app.post("/upload_file/{path_var}",summary="上传文件")
async def upload_file(*,file: UploadFile, path_var: str | None = None,code: str | None = Query(None,min_length=4,max_length=8,alias="token")):
    file_local = await save_files(file)
    return {
        "file_name": file.filename,
        "content_type": file.content_type,
        "path": path_var,
        "code": code
    }

async def save_files(file):
    path = "files"
    res = await file.read()
    hash_name = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:8]
    file_name = f"{hash_name}.{file.filename.resplit('.',1)[-1]}"
    full_file = f"{path}/{file_name}"
    with open(full_file, "wb") as f:
        f.write(res)
    return full_file
```

#### 简易网盘

```python
# FileDB.py
import dbm
from config import config

FILE_DB = "file.db"
SHARE_DB = "share.db"
dbm.open("file.db", "c")
dbm.open("share.db", "c")
class FileDB:
    def __init__(self):
        pass
    
    def create_file(self, unique_name: str, file_name: str):
        db = dbm.open(FILE_DB, 'c')
        db[unique_name] = file_name.encode('utf-8')
        db.close()
    
    def get_file(self, unique_name: str):
        db = dbm.open(FILE_DB,"r")
        files = db.keys()
        find_name = bytes(unique_name, encoding='utf-8')
        if find_name in files:
            return db.get(unique_name)
        return None
    
    def get_all_files(self):
        files = dbm.open(FILE_DB,"r")
        codes = dbm.open(SHARE_DB,"r")
        all_files = []
        for key in files.keys():
            file = {
                "file_name": str(files[key], "utf-8"),
                "unique_name": str(key, "utf-8"),
                "code": str(codes[key], "utf-8")
            }
            all_files.append(file)
            
        return all_files
    
    def get_share_code(self, unique_name: str,code: str):
        db = dbm.open(SHARE_DB, "c")
        db[unique_name] = code
        db.close()
    
    def get_share_codes(self, unique_name: str):
        db = dbm.open(SHARE_DB, "r")
        return db[unique_name]
    
file_db = FileDB()
```

```html
#share.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FastAPI开发与部署</title>
    <link href="{{ url_for('statics',path='/css/main.css')}}" rel="stylesheet">
</head>
<body>
    <h1>这是全部分享文件页面</h1>
    <article>
        <header></header>
        <section>
            <ul>
                {% for file in all_files %}
                <li>
                    <div>文件名：{{file.file_name}}</div>
                    <div>分享地址：<a href="{{url_for('file_page',unique_name=file.unique_name)}}">{{file.unique_name}}</a></div>
                    <div>分享码：<a href="{{url_for('file_page',unique_name=file.unique_name)}}?share_code={{file.code}}">{{file.code}}</a></div>
                </li>
                {% endfor %}
            </ul>
        </section>
    </article>
</body>
</html>
```

```html
# file.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FastAPI开发与部署</title>
    <link href="{{ url_for('statics',path='/css/main.css')}}" rel="stylesheet">
</head>
<body>
    <h1>这是下载页面</h1>
    <article>
        <header></header>
        <section>
            <div>
                <h3>要下载的文件</h3>
                <h4>{{file_name}}</h4>
                <form action="{{url_for('download_file',unique_name=unique_name)}}" method="post">
                    <label for="share">分享码
                    <input name="share" type="text" value="{{ share_code }}">
                    </label>
                    <button type="submit">下载</button>
                </form>
            </div>
        </section>
    </article>

</body>
</html>
```

```python
# pan.py
import os

from fastapi import APIRouter, UploadFile, Request, Form, Query,status, Path
from fastapi.responses import JSONResponse, FileResponse

from utils import unique_generation
from FileDB import file_db


router = APIRouter()
UPLOAD_DIR = "upload_dir"


@router.post("/upload_file",summary="上传文件")
async def upload_file(*,request:Request,file: UploadFile):
    unique_name = await save_files(file)
    # 将文件信息保存到dbm
    file_db.create_file(unique_name, file.filename)
    # 生成一个分享码，并保存到dbm
    share_code = unique_generation(length=6)
    file_db.create_share_code(unique_name, share_code)
    return {
        "file_name": file.filename,
        "content_type": file.content_type,
        "code": share_code,
        "url":request.url_for("file_page", unique_name=unique_name).path,
    }


@router.get("/share",summary="全部文件页面")
async def share_file(request: Request):
    all_files = file_db.get_all_files()
    data = {"all_files":all_files}
    return request.app.state.templates.TemplateResponse(request=request,name="share.html", context=data)

@router.get("/file/{unique_name}",summary="文件下载页面")
async def file_page(request: Request, unique_name: str, share_code: str | None = Query(None,min_length=6)):
    # 查询文件是否存在
    file_name = file_db.get_file(unique_name)
    # 没有找到对应的下载文件，返回404的响应
    if file_name is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"File not found"})
    if share_code is None:
        share_code = ""
    data = {
        "file_name": str(file_name,encoding="utf-8"),
        "unique_name": unique_name,
        "share_code": share_code
    }
    return request.app.state.templates.TemplateResponse(request=request,name="file.html", context=data)

@router.post("/download/{unique_name}",summary="下载文件")
async def download_file(unique_name: str, share: str = Form()):
    code = str(file_db.get_share_code(unique_name),encoding="utf-8")
    if code != share:
        return {"验证错误":"访问码错误，你无权下载该文件"}

    file_name = str(file_db.get_file(unique_name),encoding="utf-8")
    download_file = f"{unique_name}.{file_name.rsplit('.',1)[-1]}"
    file_path = UPLOAD_DIR + "/" + download_file
    return FileResponse(file_path,media_type="application/octet-stream",filename=file_name)

async def save_files(file):
    # 查看保存目录是否存在，如果不存在就创建该目录
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR,exist_ok=True)
    res = await file.read()
    # 重新生成一个分享文件名，并用此名字为上传文件重新命名
    unique_name = unique_generation()
    file_name = f"{unique_name}.{file.filename.rsplit('.',1)[-1]}"
    full_file = f"{UPLOAD_DIR}/{file_name}"
    with open(full_file, "wb") as f:
        f.write(res)
    # 返回分享文件名，以便作为分享路径的一部分
    return unique_name

```

#### APIRouter

**router.py**

```python
all_routers = APIRouter()
all_routers.include_router(pan,prefix="/api",tag="简易网盘")
```

**app.py**

```python
app.include_router(all_routers)
```

**pan.py**

```python
router = APIRouter()
```

#### 简单的认证：依赖项的使用

路径操作函数

```python
from fastapi import APIRouter, Depends

router = APIRouter()

# 这是最底层的依赖函数
def level_1():
    print("level_1")
    return 10
# 这是第二层的依赖项函数
def level_2_a(t2a: int = Depends(level_1)):
    print("level_2")
    return 20 + t2a

# 这是第二层的依赖项函数
def level_2_b(t2b: int = Depends(level_1)):
    print("level_2")
    return 40 + t2b

# 这是第三层的依赖项函数，也是最顶层
def level_3(l2a: int = Depends(level_2_a),l2b: int = Depends(level_2_b)):
    print("level_3")
    return l2a + l2b

# 这是用于接收请求里的路径查询的依赖项函数
def query_depends(user:str,token:str):
    data = {
        "user":user,
        "token":token,
    }
    return data

@router.get("/depends_show")
async def level_3(total:int =Depends(level_3),common: str = Depends(query_depends)):
    return {"total":total,"common":common}
# 类
class User:
    def __init__(self,name:str,token:str):
        self.name = name
        self.token = token

@router.get("/depends_show")
async def level_3(total:int =Depends(level_3),common: str = Depends(User)):
    return {"total":total,"name":common.name,"token":common.token}

```

路径装饰器

```python
@router.get("/depends_show",dependencies=[Depends(query_depends)])
async def level_3(common: str = Depends(User)):
    return {"name":common.name,"token":common.token}
```

我们设置检查账户权限，可以在路径装饰器中添加，如果要在所有；路由上添加，可以添加在

```python
all_routers.include_router(play,prefix="/play", tags=["依赖项"],dependencies=[Depends(check_user)])
```

#### FastAPI里Security的使用

```python
from fastapi import APIRouter, Security
from fastapi.security import SecurityScopes

router = APIRouter()

def print_scopes(security_scopes:SecurityScopes):
    print(security_scopes.scopes)

@router.get("/group/admin",dependencies=[Security(print_scopes,scopes=['admin'])])
async def group_admin():
    pass

@router.get("/group/user",dependencies=[Security(print_scopes,scopes=['users'])])
async def group_user():
    pass

@router.get("/guest",dependencies=[Security(print_scopes,scopes=['guest'])])
async def group():
    pass
```



设置权限

```python
def get_user_token(pan_token: str | None = Cookie(default=None)):
    return pan_token

def get_user_permission(token: str = Depends(get_user_token)):
    if token == 'Tai_admin':
        return 'admin'
    if token == 'Tai_user':
        return 'users'
    return None


def check_user(security_scopes:SecurityScopes,user_permission: str = Depends(get_user_permission)):
    print(security_scopes.scopes)
    if user_permission not in security_scopes.scopes:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="你没有权限执行该操作")

# admin上传文件

@router.post("/upload_file",summary="上传文件",dependencies=[Security(check_user,scopes=['admin'])])
async def upload_file(*,request:Request,file: UploadFile):
    unique_name = await save_files(file)
    # 将文件信息保存到dbm
    file_db.create_file(unique_name, file.filename)
    # 生成一个分享码，并保存到dbm
    share_code = unique_generation(length=6)
    file_db.create_share_code(unique_name, share_code)
    return {
        "file_name": file.filename,
        "content_type": file.content_type,
        "code": share_code,
        "url":request.url_for("file_page", unique_name=unique_name).path,
    }
    
    #只能users下载文件
   @router.post("/download/{unique_name}",summary="下载文件",dependencies=[Security(check_user,scopes=['user'])])
async def download_file(unique_name: str, share: str = Form()):
    code = str(file_db.get_share_code(unique_name),encoding="utf-8")
    if code != share:
        return {"验证错误":"访问码错误，你无权下载该文件"}

    file_name = str(file_db.get_file(unique_name),encoding="utf-8")
    download_file = f"{unique_name}.{file_name.rsplit('.',1)[-1]}"
    file_path = UPLOAD_DIR + "/" + download_file
    return FileResponse(file_path,media_type="application/octet-stream",filename=file_name)
```

#### 基于角色的权限控制

```python
ALL_USERS ={
    'JACK':['admin','users'],
    'rose':['admin','users'],
    'tom': ['users'],
    'jerry': ['users']
}

ALL_PERMISSIONS = {
    'admin':['upload'],
    'users':['visit','download'],
}

def get_user_token(user_name: str | None = Cookie(default=None)):
    print(user_name)
    if user_name is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user_name is required")
    return user_name

def get_role_permission(role_names: List[str]):
    permissions = []
    for role_name in role_names:
        for perm in ALL_PERMISSIONS[role_name]:
            permissions.append(perm)
    return permissions

def get_user_permission(user_name: str = Depends(get_user_token)):
    if user_name in ALL_USERS:
        return get_role_permission(ALL_USERS[user_name])
    return None


def check_user(security_scopes:SecurityScopes,user_permission: str = Depends(get_user_permission)):
    for scope in security_scopes.scopes:
        # 检查路径接口需要的权限是否存在用户对应的所有权限
        if scope not in user_permission:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="你没有权限执行该操作")
```

#### JWT

```bash
pip install pyjwt
```

**生成密钥**

```bash
openssl rand -hex 32
```

auth.py

```python
"""
JWT 其实定义了一种基于 Token 的会话方式，也就是通过一种规则说明了
使用这种Token的标准以及 Token 如何生成和解码
我们就是通过代码来实现这个会话规则
"""
from datetime import datetime, timezone, timedelta

import jwt
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = 'a5343793350d75f4c326095ce8b9d735c5544d7a60bd29e71e07067eeb8358e4'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE = 30


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")

def create_token(data:dict):
    to_encode = data.copy()
    to_encode.update({'exp': datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)})
    encode_jwt = jwt.encode(
        to_encode, # 要通过Token传输的内容!!!不要放敏感信息
        SECRET_KEY,# JWT签名的密钥
        algorithm=ALGORITHM # JWT签名的算法
    )
    return encode_jwt
def verify_token(token:str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Token expired',headers={'WWW-Authenticate':'Bearer'})
    return payload
```

pan.py

```python
@router.get("/send_token")
async def send_token(response: Response):
    data = {"username": "Jack"}
    token = create_token(data)
    return token

@router.get("/get_token")
async def get_token(data=Depends(verify_token)):
    return data
```

#### 中间件

```python
# 第一道关卡：中间件能第一时间获取请求，根据需要对其处理
@app.middleware('http')
async def add_headers(request: Request, call_next):
    print(f"获取到了请求路径：{request.url}")
    response = await call_next(request)
    return response

# 最后的关卡：中间件在响应返回前对响应进行处理
@app.middleware('http')
async def index(request: Request,call_next):
    response = await call_next(request)
    print("获取到了响应结果："+response.headers['Content-Type'])
    return response
```



```python
import logging
import time
from collections import defaultdict

from fastapi import Depends, FastAPI, Request, Response
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("uvicorn.access")
logger.disabled = True
def my_logger(message):
    print(message)

def tai_middleware(app: FastAPI):
    # 打印每个请求所用时间
    @app.middleware("http")
    async def count_time(request: Request,call_next):
        start_time = time.time()
        response = await call_next(request)
        response_time = time.time() - start_time
        print(response_time)
        return response

    @app.middleware("http")
    async def tai_logging(request: Request,call_next):
        message = f"{request.client.host}:{request.client.port} {request.method} {request.url.path}"
        my_logger(message)
        response = await call_next(request)
        return response

    # 访问速率限制的中间件
    class RateLimitMiddleware(BaseHTTPMiddleware):
        def __init__(self, app: FastAPI):
            super().__init__(app)
            self.request_records: dict[str,float] = defaultdict(float)
            self.counter = 0

        async def dispatch(self, request: Request, call_next):
            ip = request.client.host # 获取客户端的IP
            current_time = time.time() # fastapi接收到客户端请求的时间
            self.counter += 1
            print(self.counter)
            if current_time - self.request_records[ip] < 5:
                return Response(content="超过访问限制",status_code=429)

            response = await call_next(request)
            self.request_records[ip] = current_time # 成功响应，就将请求ip和请求时间保存在字典
            return response

    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], expose_headers=["*"])
```



#### lifespan加载服务

```python
@asynccontextmanager
async def tai_init(app: FastAPI):
    # 启动时执行的事件
    print("Tai启动啦")
    # logger_init() 启动日志服务
    # db_init() 连接数据库
    # service_close() 退出第三方服务
    # send_email() 发送email给我们的程序维护者
    yield print("我是生命周期事情，等待下一次被使用")
    # 终止时执行的事情
    # logger() 记录关闭日志
    # db_close() 关闭数据库连接
    # service_close() 退出第三方服务
    # send_email() 发送email给我们的程序维护者
    print("Tai关闭啦")

app = FastAPI(
    debug=config.DEBUGE_MODE,
    lifespan=tai_init
)

```

#### redis

```bash
pip install redis>=5.1.0 # 支持python3.12
```

**main.py**

```python
from database.redis import redis_connect

@asynccontextmanager
async def tai_init(app: FastAPI):
    # 启动时执行的事件
    print("Tai启动啦")
    app.state.redis = await redis_connect()
    # logger_init() 启动日志服务
    # db_init() 连接数据库
    # service_close() 退出第三方服务
    # send_email() 发送email给我们的程序维护者
    yield print("我是生命周期事情，等待下一次被使用")
    # 终止时执行的事情
    app.state.redis.close()
    # logger() 记录关闭日志
    # db_close() 关闭数据库连接
    # service_close() 退出第三方服务
    # send_email() 发送email给我们的程序维护者
    print("Tai关闭啦")
```

```python
# playground.py
@router.get("/redis")
async def redis_set(request: Request):
    value = await request.app.state.redis.get('fastapi_redis')

    # 如果没有被redis缓存
    if value is None:
        sleep(5)
        hi = 'hey,redis!'
        await request.app.state.redis.set(
            'fastapi_redis', # 键名
            hi,             # 键值
            ex=60           # 多少秒过期
        )
        return hi

    return value
```

#### WebSocket

```python
# 注意请求方法是websocket
@router.websocket("/ws2")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 接收信息
            message = await websocket.receive_text()

            # 输出信息
            await websocket.send_text(message)
    except WebSocketDisconnect:
        print('websocket disconnect')

```

