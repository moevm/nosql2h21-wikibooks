from neo4j import GraphDatabase, Result

class DBMS:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))


    def close(self):
        self.driver.close()


    def _make_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return result.data()


    def add_book(self, lang):
        query = "LOAD CSV WITH HEADERS from \'file:///" + lang + ".csv\' as row with row where row.title is not null MERGE(b:Wikibook {title: row.title, url: row.url,html: row.body_html, message: \"" + lang + "\"}) RETURN b"
        res = self._make_query(query)
        self.add_rels(lang)


    def add_rels(self, lang):
        query = "MATCH(a: Language{message: \'" + lang + "\'}),(b:Wikibook {message: \'" + lang + "\'}) CREATE(a) - [r: translated_in]->(b)"
        res = self._make_query(query)


    def get_book(self, lang):
        query = "MATCH(a: Wikibook{message: \'" + lang + "\'}) RETURN a.title"
        data = self._make_query(query)
        books = set(map(lambda el: el["a.title"], data))
        print(books)


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


if __name__ == "__main__":
    greeter = DBMS("bolt://localhost:7687", "neo4j", "123")
    greeter.print_language("de")
    greeter.print_language("en")
    greeter.print_language("es")
    greeter.print_language("fr")
    greeter.print_language("he")
    greeter.print_language("hu")
    greeter.print_language("it")
    greeter.print_language("ja")
    greeter.print_language("nl")
    greeter.print_language("pl")
    greeter.print_language("pt")
    greeter.print_language("ru")
    greeter.add_book("de")
    greeter.add_book("en")
    greeter.add_book("es")
    greeter.add_book("fr")
    greeter.add_book("he")
    greeter.add_book("hu")
    greeter.add_book("it")
    greeter.add_book("ja")
    greeter.add_book("nl")
    greeter.add_book("pl")
    greeter.add_book("pt")
    greeter.add_book("ru")
    greeter.get_book("ru")
    greeter.close()