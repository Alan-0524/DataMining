import mysql.connector
import xlrd


def read_file():
    try:
        data = xlrd.open_workbook('D:\publicly-funded-discharges-2014_15-static-071117.xlsx')
        return data
    except Exception as e:
        print(str(e))


mydb = mysql.connector.connect(
    host="localhost",
    user="rm",
    passwd="000000",
    database="mydb"
)


def print_file():
    data = read_file()
    table = data.sheet_by_name("Discharges - All")  # 获得表格
    total_rows = table.nrows  # 拿到总共行数
    diseaseName = ""
    dischargeYear = "2014-2015"
    list = []
    x = 0
    mycursor = mydb.cursor()
    sql = "INSERT INTO discharge (year,dischargeName,gender,meanStay,total,dayCases,age0,age5,age10,age15,age20,age25,age30,age35,age40,age45,age50,age55,age60,age65,age70,age75,age80,age85) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for i in range(total_rows):  # 循环逐行打印
        if i < 11:
            continue
        else:
            if table.cell(i, 0).value is not "":
                diseaseName = table.cell(i, 0).value
                continue
            else:
                x = x + 1
                discharge = type("Discharge", (object,), {})
                discharge.year = dischargeYear
                discharge.diseaseName = diseaseName.__str__().strip()
                discharge.gender = str(table.cell(i, 1).value).replace(" ", "").replace(":", "")
                discharge.meanStay = str(table.cell(i, 2).value).replace(" ", "")
                discharge.total = str(table.cell(i, 3).value).replace(" ", "")
                discharge.dayCases = str(table.cell(i, 4).value).replace(" ", "")
                discharge.age0 = str(table.cell(i, 5).value).replace(" ", "")
                discharge.age5 = str(table.cell(i, 6).value).replace(" ", "")
                discharge.age10 = str(table.cell(i, 7).value).replace(" ", "")
                discharge.age15 = str(table.cell(i, 8).value).replace(" ", "")
                discharge.age20 = str(table.cell(i, 9).value).replace(" ", "")
                discharge.age25 = str(table.cell(i, 10).value).replace(" ", "")
                discharge.age30 = str(table.cell(i, 11).value).replace(" ", "")
                discharge.age35 = str(table.cell(i, 12).value).replace(" ", "")
                discharge.age40 = str(table.cell(i, 13).value).replace(" ", "")
                discharge.age45 = str(table.cell(i, 14).value).replace(" ", "")
                discharge.age50 = str(table.cell(i, 15).value).replace(" ", "")
                discharge.age55 = str(table.cell(i, 16).value).replace(" ", "")
                discharge.age60 = str(table.cell(i, 17).value).replace(" ", "")
                discharge.age65 = str(table.cell(i, 18).value).replace(" ", "")
                discharge.age70 = str(table.cell(i, 19).value).replace(" ", "")
                discharge.age75 = str(table.cell(i, 20).value).replace(" ", "")
                discharge.age80 = str(table.cell(i, 21).value).replace(" ", "")
                discharge.age85 = str(table.cell(i, 22).value).replace(" ", "")
                list.append(discharge)
    for discharge in list:
        val = (discharge.year, discharge.diseaseName, discharge.gender, discharge.meanStay, discharge.total,
               discharge.dayCases,
               discharge.age0, discharge.age5, discharge.age10, discharge.age15, discharge.age20, discharge.age25,
               discharge.age30, discharge.age35, discharge.age40, discharge.age45, discharge.age50, discharge.age55,
               discharge.age60, discharge.age65, discharge.age70, discharge.age75, discharge.age80, discharge.age85)
        print(discharge.diseaseName)
        mycursor.execute(sql, val)

    mydb.commit()


# sql = "INSERT INTO discharge VALUES ('2005-2006', 'A00-B99  I     Certain infectious and parasitic diseases', 'Total:',4.4,20055,6351,7075,1278,828,1124,1035,761,753,713,736,776,722,700,598,632,604,596,540,584)"


print_file()
# columns = table.row_values(column_name)  # 某一行数据 ['姓名', '用户名', '联系方式', '密码']
# excel_list = []
# for one_row in range(1, total_rows):  # 也就是从Excel第二行开始，第一行表头不算
#
#     row = table.row_values(one_row)
#     if row:
#         row_object = {}
#         for i in range(0, len(columns)):
#             key = table_header[columns[i]]
#             row_object[key] = row[i]  # 表头与数据对应
#
#         excel_list.append(row_object)
#
# return excel_list
