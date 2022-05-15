# typecho api调用
from pytypecho import Post, Typecho


class TypechoXmlRpcPublisher:
    def __init__(self, xmlrpc_url, username, password):
        self.__typecho = Typecho(xmlrpc_url, username=username, password=password)

    def publish_post(self, title, content):
        post = Post(title=title, description=content)
        return self.__typecho.new_post(post, publish=True)
