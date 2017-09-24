from whoosh.fields import TEXT, Schema
from whoosh.index import open_dir, create_in
from whoosh.qparser import QueryParser
from os import mkdir
from app import app
from app.controller.usercontroller import session
from app.models.models import Posts


def create_index(user_id, post_id, nickname, post_body):
    schema = Schema(user_id=TEXT(stored=True),
                    post_id=TEXT(stored=True),
                    nickname=TEXT(stored=True),
                    content=TEXT(stored=True))

    try:
        ix = open_dir(app.config['WHOOSH_BASE'])

    except:
        mkdir(app.config['WHOOSH_BASE'])
        ix = create_in(app.config['WHOOSH_BASE'], schema)

    writer = ix.writer()
    print(str(user_id), str(post_id), nickname, post_body)
    writer.add_document(user_id=str(user_id),
                        post_id=str(post_id),
                        nickname=nickname,
                        content=post_body)
    writer.commit()


def query(key):
    rt = []
    try:
        ix = open_dir(app.config['WHOOSH_BASE'])
        with ix.searcher() as searcher:
            query_key = QueryParser('content', ix.schema).parse(key)
            print("query_key:", query_key)

            results = searcher.search_page(query_key, 1, app.config['MAX_SEARCH_RESULTS'], sortedby='post_id',
                                           reverse=True)
            #results = searcher.search(query_key)

            print(results)
            for item in results:
                user_id = item.fields()['user_id']
                post_id = item.fields()['post_id']
                nickname = item.fields()['nickname']
                post_body = item.fields()['content']
                rt.append({'user_id': int(user_id),
                           'post_id': int(post_id),
                           'nickname': nickname,
                           'post_body': post_body})
    except:
        print('There is no post exist!')

    finally:
        return rt


if __name__ == '__main__':

    posts = session.query(Posts).all()
    for post in posts:
        session.delete(post)
        session.commit()
        session.close()


