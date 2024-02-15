from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import sqlite3 


cnt = sqlite3.connect("users.db") 

class MainHandler(RequestHandler):
    def get(self):
        self.write('REST API')
        
        
class UserInfoHandler(RequestHandler):

    def  post(self):
        id =  self.get_argument('id')
        name = self.get_argument('name')
        cnt.execute(f"insert into users values({id}, '{name}');")
        cnt.commit()

        cursor = cnt.execute(f"select id,name from users where id=={id}")
        
        for i in cursor: 
            self.write({'id':i[0], 'name':i[1]})
          
    
    def get(self):
        id = self.get_argument('id') 
        userdict = {}
        cursor = cnt.execute(f"select id,name from users where id=={id}")
        for i in cursor: 
            userdict.update({'id':i[0],'name':i[1]})
        
        self.write(userdict)

    def put(self):
        id = self.get_argument('id')
        name = self.get_argument('name')
        cnt.execute(f"update users set name='{name}' where id={id};")
        cnt.commit()

        
        cursor = cnt.execute(f"select id,name from users where id=={id}")
        for i in cursor: 
            self.write({'id':i[0],'name':i[1]})
        

    def delete(self):
        id = self.get_argument('id')
        cnt.commit()

        
        cnt.execute(f"delete from users where id=={id};")
        self.write(f'user {id} is deleted')
        

def make_app():
  urls = [
    (r"/", MainHandler),
    (r"/user",UserInfoHandler)
  ]
  return Application(urls, debug=True)


if __name__ == '__main__':
  app = make_app()
  app.listen(3002)
  IOLoop.instance().start()

