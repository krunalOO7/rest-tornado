from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import sqlite3 


 

class MainHandler(RequestHandler):
    def get(self):
        self.write('REST API')
        
        
class UserInfoHandler(RequestHandler):

    def  post(self):
        
        id =  self.get_argument('id')
        name = self.get_argument('name')
        cnt = sqlite3.connect("users.db")
        try:
            cursor=cnt.execute(f'select * from users where ID={id}')
            result = cursor.fetchone()

            if(not result is None):
                self.write(f'user with user id{id} already exist please select deferent id')
                

            else:
                cnt.execute(f"insert into users values({id}, '{name}');")
                cnt.commit()
                self.write(f'{id}: {name} added successfully\n')
        except:
            self.write("something went wrong please try again letter!")


          
    
    def get(self):
        
        id = self.get_argument('id') 
        try:
            cnt = sqlite3.connect("users.db")
            cursor = cnt.execute(f"select * from users where id=={id}")  
            res = cursor.fetchone()
            
            if(not res is None):
                self.write({res[0]:res[1]})
        
            else:
                self.write(f'no user found with given id:{id}')

        except:
            self.write("something went wrong!")
            

    def put(self):
        
        id = self.get_argument('id')
        name = self.get_argument('name')
        try:
            cnt = sqlite3.connect("users.db")
            cursor = cnt.execute(f'select * from users  where id={id}')
            res = cursor.fetchone()
            if(not res is None):
                cnt.execute(f"update users set name='{name}' where id={id};")
                cnt.commit()
                self.write(f'user name {name} has been updated successfully!')
            else:
                self.write(f'No User Found With Given Id : {id} ')
        except:
            print("something  went wrong!")
       
        

    def delete(self):
        
        id = self.get_argument('id')
        try:

            cnt = sqlite3.connect("users.db")
            cursor = cnt.execute(f"select id,name from users where id=={id}")  
            res = cursor.fetchone()
            
            
            if(res is None):
                self.write(f'no user found with given id:{id}')
            
            else:
                cnt.execute(f"delete from users where id=={id};")
                self.write(f'user {id} is deleted')
                cnt.commit()
        except:
            print("something went wrong!")
        
        

def make_app():
  urls = [
    (r"/", MainHandler),
    (r"/user",UserInfoHandler)
  ]
  return Application(urls, debug=True)


if __name__ == '__main__':
  app = make_app()
  app.listen(3000)
  IOLoop.instance().start()


