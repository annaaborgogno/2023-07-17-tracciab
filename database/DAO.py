

from database.DB_connect import DBConnect
from model.edge import Edge
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getBrands():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select distinct gp.Product_brand as brand 
                    from go_products gp  """

        cursor.execute(query, )

        for row in cursor:
            res.append(row["brand"])
        conn.close()
        cursor.close()
        return res

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select DISTINCT  YEAR(gds.`Date`) as year
                    from go_daily_sales gds 
                    order by year asc """

        cursor.execute(query, )

        for row in cursor:
            res.append(row["year"])
        conn.close()
        cursor.close()
        return res

    @staticmethod
    def getNodes(brand):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select *
                    from go_products gp 
                    where gp.Product_brand = %s"""

        cursor.execute(query, (brand,))

        for row in cursor:
            res.append(Product(**row))
        conn.close()
        cursor.close()
        return res

    @staticmethod
    def getEdges(brand, year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select least(gp1.Product_number, gp2.Product_number) as prod1, greatest(gp1.Product_number, gp2.Product_number) as prod2, count(distinct gds1.Retailer_code) as peso
                    from go_products gp1, go_products gp2, go_daily_sales gds1, go_daily_sales gds2
                    where gp1.Product_number != gp2.Product_number 
                    and gp1.Product_brand = gp2.Product_brand
                    and gp1.Product_brand = %s
                    and gds1.Product_number = gp1.Product_number
                    and gds2.Product_number = gp2.Product_number
                    and gds1.Retailer_code = gds2.Retailer_code
                    and gds1.`Date` = gds2.`Date`
                    and YEAR(gds1.`Date`) = %s
                    group by prod1, prod2
                    order by peso desc"""

        cursor.execute(query, (brand, year))

        for row in cursor:
            res.append(Edge(**row))
        conn.close()
        cursor.close()
        return res

