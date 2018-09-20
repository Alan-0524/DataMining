import mysql.connector


class MySqlConnector:
    pass
    conn = None  # 这里的None相当于其它语言的NULL

    def __init__(self):  # 构造函数
        self.conn = mysql.connector.connect(host="localhost", user="rm", passwd="000000", database="mydb")

    def getBySql(self, year, gender):
        row_total = "100"
        set_duplicates = self.remove_duplicates(year, gender, row_total)
        sql = "SELECT t.* FROM discharge t "
        if year is not "" and gender is not "":
            sql = sql + "WHERE t.year = '" + year + "' and t.gender = '" + gender + "'"
        if year is not "" and gender is "":
            sql = sql + "WHERE t.year = '" + year + "'"
        if year is "" and gender is not "":
            sql = sql + "WHERE t.gender = '" + gender + "'"
        sql = sql + "and t.total>"+row_total+" and t.key not in ("+set_duplicates+")"
        mycursor = self.conn.cursor()
        mycursor.execute(sql)
        results = mycursor.fetchall()
        # self.conn.commit();
        mycursor.close()
        print(year, "total:" + len(results).__str__())
        return results

    def remove_duplicates(self, year, gender, row_total):
        sql = "SELECT  t1.key,substring(t1.dischargeName,1,3) as disease_code FROM discharge t1, discharge t2"
        sql = sql+" where t1.age0 = t2.age0"
        sql = sql+" and t1.age5 = t2.age5"
        sql = sql+" and t1.age10 = t2.age10"
        sql = sql+" and t1.age15 = t2.age15"
        sql = sql+" and t1.age20 = t2.age20"
        sql = sql+" and t1.age25 = t2.age25"
        sql = sql+" and t1.age30 = t2.age30"
        sql = sql+" and t1.age35 = t2.age35"
        sql = sql+" and t1.age40 = t2.age40"
        sql = sql+" and t1.age45 = t2.age45"
        sql = sql+" and t1.age50 = t2.age50"
        sql = sql+" and t1.age55 = t2.age55"
        sql = sql+" and t1.age60 = t2.age60"
        sql = sql+" and t1.age65 = t2.age65"
        sql = sql+" and t1.age70 = t2.age70"
        sql = sql+" and t1.age75 = t2.age75"
        sql = sql+" and t1.age80 = t2.age80"
        sql = sql+" and t1.age85 = t2.age85"
        sql = sql+" and t1.key != t2.key"
        sql = sql+" and t1.year = '"+year+"'"
        sql = sql+" and t2.year = '"+year+"'"
        sql = sql+" and t1.gender = '"+gender+"'"
        sql = sql+" and t2.gender = '"+gender+"'"
        sql = sql+" and t1.total>"+row_total+""
        sql = sql+" and t2.total>"+row_total+""
        sql = sql+" and t1.dischargeName not like '%-%'"
        sql = sql+" and t2.dischargeName not like '%-%'"
        sql = sql+" order by t1.key asc"
        mycursor = self.conn.cursor()
        mycursor.execute(sql)
        list_results = mycursor.fetchall()
        set_key = ''
        mycursor.close()
        for i in range(0, len(list_results)):
            for j in range(i+1, len(list_results)):
                if list_results[i][1] == list_results[j][1]:
                    set_key += str(list_results[j][0])+","
        return set_key[:-1]

# db = MySqlConnector()
# db.getBySql("2005-2006", "Total")
