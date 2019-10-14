from sqlalchemy.orm import sessionmaker
from models import Corals, db_connect, create_corals_table


class Pipeline(object):

    def __init__(self):
        engine = db_connect()
        print(engine)
        create_corals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item):

        session = self.Session()
        coral = Corals(**item)
        
        try:
            session.add(coral)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        print(item)
        return item
