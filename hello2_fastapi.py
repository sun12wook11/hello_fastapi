from fastapi import FastAPI
# fastapi 앱 실행 방법

app = FastAPI()
@app.get("/")
def index():

    return "Hello World, again!!"

# __name__: 실행중인 모듈이름을 의미하는 매직키워드
# 만일, 파일을 직접 실행하면 __name__의 이름은 __main__으로 자동지정
if __name__ == "__main__":
    import uvicorn
    uvicorn.run('hello2_fastapi:app', reload=True)
