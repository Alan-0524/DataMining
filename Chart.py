import Levenshtein
import MySqlConnector
from collections import Counter


def getresult(year, gender, convergence, d_val, calculation_type):
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
        if calculation_type == 0:
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
        if calculation_type == 1:
            for j in range(7, 24):
                if float(discharge[j]) != 0:
                    val = (float(discharge[j + 1]) - float(discharge[j])) / float(discharge[j])
                    list_set.append(val)
                else:
                    list_set.append("infinite")
            if list_set.count("infinite") <= convergence:
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
            if calculation_type == 0:
                diff_val = Levenshtein.seqratio(set_a, set_b)
                if filter_inclusion(name_a[0], name_b[0]) is True and diff_val >= d_val:
                    list_tmp = [name_a, name_b, set_a, set_b, diff_val]
                    list_top.append(list_tmp)
            if calculation_type == 1:
                range_abs = determine_abs(set_a, set_b, d_val)
                if filter_inclusion(name_a[0], name_b[0]) is True and range_abs is True:
                    list_tmp = [name_a, name_b, set_a, set_b]
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


def determine_abs(set_a, set_b, d_val):
    count = 0
    for i in range(0, len(set_a)):
        if set_a[i] == "infinite" or set_b[i] == "infinite":
            pass
        else:
            if (set_a[i] >= 0 and set_b[i] >= 0) or (set_a[i] <= 0 and set_b[i] <= 0):
                diff_val = abs(set_a[i] - set_b[i])
                if diff_val > d_val:
                    return False
            else:
                count = count+1
                if count > 1:
                    return False
                else:
                    diff_val = abs(set_a[i] - set_b[i])
                    if diff_val > d_val:
                        return False
    return True


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
        # list_g = getresult(year, t, 2, 0.94, 0)
        list_g = getresult(year, t, 2, 0.6, 1)
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
# a = ['0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1']
# b = ['0', '0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
#
# print(Levenshtein.seqratio(a, b))
