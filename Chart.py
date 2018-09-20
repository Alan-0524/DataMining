import matplotlib.pyplot as plt
import Levenshtein
import MySqlConnector
from collections import Counter


def getresult(year, gender, convergence, d_val):
    connector = MySqlConnector.MySqlConnector()
    results = connector.getBySql(year, gender)
    diff = 0
    list_ = []
    list_top = []
    list_bottom = []
    for discharge in results:
        list_whole = []
        list_name = []
        list_set = []
        list_name.append(str(discharge[2]))
        for j in range(7, 24):
            val = float(discharge[j + 1]) - float(discharge[j])
            if val > 0:
                diff = 1
            elif val < 0:
                diff = -1
            elif val == 0:
                diff = 0
            list_set.append(diff.__str__())
        if list_set.count("0") <= convergence:
            list_whole.append(list_name)
            list_whole.append(list_set)
            list_.append(list_whole)
    for i in range(0, len(list_)):
        for j in range(i + 1, len(list_)):
            name_a = list_.__getitem__(i).__getitem__(0)
            name_b = list_.__getitem__(j).__getitem__(0)
            set_a = list_.__getitem__(i).__getitem__(1)
            set_b = list_.__getitem__(j).__getitem__(1)
            # print("-------------------------start-------------------------")
            # print(name_a, name_b)
            # print("set_a:", set_a)
            # print("set_b:", set_b)
            # print("-------------------", Levenshtein.seqratio(set_a, set_b), "-------------------")
            diff_val = Levenshtein.seqratio(set_a, set_b)
            if filter_inclusion(name_a[0], name_b[0]) is True and diff_val >= d_val:
                list_tmp = [name_a, name_b, set_a, set_b, diff_val]
                list_top.append(list_tmp)
            # if diff_val < 0.06:
            #     list_tmp = [name_a, name_b, diff_val]
            #     list_bottom.append(list_tmp)
    # print("--------------------------------------Top total:", len(list_top), "--------------------------------------")
    list_count = []
    for discharge in list_top:
        # print(year, "disease_a:", discharge[0], "disease_b:", discharge[1])
        code_a = str(discharge[0][0]).split(" ").__getitem__(0).upper()
        code_b = str(discharge[1][0]).split(" ").__getitem__(0).upper()
        str_disease = code_a + "," + code_b
        list_count.append(str_disease)
        # print("set_a:", discharge[2], "set_b:", discharge[3])
        # print("diff_val:", discharge[4])
    # print("--------------------------------------------bottom--------------------------------------------")
    return list_count
    # for discharge in list_bottom:
    #     print("set_a:", discharge[0], "set_b:", discharge[1], "diff_val:", discharge[2])


def filter_inclusion(name_a, name_b):
    code_a = str(name_a).split(" ").__getitem__(0)
    code_b = str(name_b).split(" ").__getitem__(0)
    if code_a.find("-") != -1 and code_b.find("-") != -1:
        list_code_a = code_a.split("-")
        code_left_letter_a = list_code_a[0].__str__()[0:1]
        code_left_number_a = list_code_a[0].__str__()[1:len(list_code_a[0])]
        code_right_letter_a = list_code_a[1].__str__()[0:1]
        code_right_number_a = list_code_a[1].__str__()[1:len(list_code_a[1])]

        list_code_b = code_b.split("-")
        code_left_letter_b = list_code_b[0].__str__()[0:1]
        code_left_number_b = list_code_b[0].__str__()[1:len(list_code_b[0])]
        code_right_letter_b = list_code_b[1].__str__()[0:1]
        code_right_number_b = list_code_b[1].__str__()[1:len(list_code_b[1])]

        if code_left_letter_a != code_left_letter_b:
            return True
        if code_left_letter_a == code_left_letter_b and int(
                code_left_number_a) <= int(code_left_number_b) <= int(code_right_number_a):
            return False
        else:
            return True

    if code_a.find("-") != -1 and code_b.find("-") == -1:
        list_code_a = code_a.split("-")
        code_left_letter_a = list_code_a[0].__str__()[0:1]
        code_left_number_a = list_code_a[0].__str__()[1:len(list_code_a[0])]
        code_right_letter_a = list_code_a[1].__str__()[0:1]
        code_right_number_a = list_code_a[1].__str__()[1:len(list_code_a[1])]

        code_letter_b = code_b[0:1]
        code_number_b = code_b[1:len(code_b)]

        if code_left_letter_a != code_letter_b:
            return True
        if int(code_left_number_a) <= int(code_number_b) <= int(code_right_number_a):
            return False
        else:
            return True

    if code_a.find("-") == -1 and code_b.find("-") != -1:
        list_code_b = code_b.split("-")
        code_left_letter_b = list_code_b[0].__str__()[0:1]
        code_left_number_b = list_code_b[0].__str__()[1:len(list_code_b[0])]
        code_right_letter_b = list_code_b[1].__str__()[0:1]
        code_right_number_b = list_code_b[1].__str__()[1:len(list_code_b[1])]

        code_letter_a = code_a[0:1]
        code_number_a = code_a[1:len(code_a)]

        if code_left_letter_b != code_letter_a:
            return True
        if int(code_left_number_b) <= int(code_number_a) <= int(code_right_number_b):
            return False
        else:
            return True

    if code_a.find("-") == -1 and code_b.find("-") == -1:
        if code_a != code_b:
            return True
        else:
            return False


def count_frequence():
    years = ["2005-2006", "2006-2007", "2007-2008", "2008-2009", "2009-2010", "2010-2011", "2011-2012", "2012-2013",
             "2013-2014", "2014-2015"]
    m = "Male"
    f = "Female"
    t = "Total"
    list_count_sort = []
    for year in years:
        list_g = getresult(year, m, 2, 0.94)
        print(year, Counter(list_g))
        list_count_sort.extend(list_g)

    print("element_total:", len(list_count_sort))
    result = Counter(list_count_sort)
    print(result)
    # for i in result:
    #     print(i[0], i[1])

count_frequence()
# a = ["A00-B00", "A00-B00", "A00-B00", "A00-B00", "A00-B00"]
# result = Counter(a)
# print(result)
# print(filter_inclusion("C00-D48", "C43-C44"))

# a = ['0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1']
# b = ['0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
#
# print(Levenshtein.seqratio(a, b))
# plt.figure(figsize=(9,6))  # fig的宽高
#
# # The slices will be ordered and plotted counter-clockwise.
# labels = [u'直接访问', u'外部链接', u'搜索引擎']
# sizes = [160, 130, 110] # sum(sizes)不一定是100，会自动按照百分比调整
# colors = ['yellowgreen', 'gold', 'lightskyblue']
#
# #explode 爆炸出来
# explode = (0.05, 0.0, 0.0)  # 间距
#
# patches, l_texts, p_texts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, labeldistance=0.8,
#         autopct='%3.1f%%', shadow=True, startangle=90, pctdistance=0.6)
#
# plt.axis('equal') # 设置x，y轴刻度一致，这样饼图才能是圆的
# plt.legend()
#
# """
# # 设置labels和百分比文字大小
# for t in l_texts:
#     t.set_size(20)
#
# for t in p_texts:
#     t.set_size(20)
# """
# plt.show()
