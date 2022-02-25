from neo4j import GraphDatabase, Result

class DBMS:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_book(self, lang):
        query = "LOAD CSV WITH HEADERS from \'file:///" + lang + ".csv\' as row with row where row.title is not null MERGE(b:Wikibook {title: row.title, url: row.url,html: row.body_html, message: \"" + lang + "\"}) RETURN b"
        res = self._make_query(query)
        self.add_rels(lang)

    def add_rels(self, lang):
        query = "MATCH(a: Language{message: \'" + lang + "\'}),(b:Wikibook {message: \'" + lang + "\'}) CREATE(a) - [r: translated_in]->(b)"
        res = self._make_query(query)

    def get_book(self, lang):
        query = "MATCH(a: Wikibook{message: \'" + lang + "\'}) RETURN a.title, a.url, a.massage, a.html"
        data = self._make_query(query)
        return(data)

    def print_language(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_language, message)
            print(greeting)

    @staticmethod
    def _create_and_return_language(tx, message):
        result = tx.run("CREATE (a:Language) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    def DELETE_ALL_RELATIONSHIPS(self):
        query = "MATCH (n)-[r]->(m) DELETE r,n,m"
        return self._make_query(query)

    def DELETE_NODES(self):
        query = "MATCH (n) DELETE n"
        return self._make_query(query)

    def _make_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return result.data()