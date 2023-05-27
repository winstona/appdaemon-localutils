import redis


class PersistentData:
  def __init__(self, app_name, app):
    print("testing init 6")
    app.log("testing init 2 - 6")

    self.redis_conn = redis.Redis(host='redis')
    self.app_name = app_name
    self.app = app

  def get(self, key, *args, **kwargs):
    #self.app.log(f"reading key: {self.app_name}-{key}")
    return self.redis_conn.get(f"{self.app_name}-{key}", *args, **kwargs)

  def set(self, key, *args, ttl=None, **kwargs):
    #self.app.log(f"kwargs: {kwargs}")
    #print(f"filtered kwargs: {{x: kwargs[x] for x in kwargs if x not in ['ttl']}}")
    #return
    #self.app.log(f"writing key: {self.app_name}-{key}")
    resp = self.redis_conn.set(f"{self.app_name}-{key}", *args,  **kwargs)
    if ttl is not None:
      self.redis_conn.expire(f"{self.app_name}-{key}", ttl)
    return resp
