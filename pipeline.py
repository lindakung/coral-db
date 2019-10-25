from sqlalchemy.orm import sessionmaker
from models import Corals, db_connect, create_corals_table


class CoralPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_corals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item):

        session = self.Session()
        coral = Corals(**item)
        
        try:
            session.add(coral)
            session.commit()
            print('{} added'.format(coral.name))
        except Exception as e:
            session.rollback()
            # raise e
        finally:
            session.close()

        return item
