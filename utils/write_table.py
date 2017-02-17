import xlwt

def output(filename, sheet, var_list, col_names):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)

    for index, name in enumerate(col_names):
        sh.write(0, index, name)

    for n in range(var_list[0]):
        for m in range(var_list):
            sh.write(n+1, 0, str(col_names[n])+" topics")
            sh.write(n+1, m+1, var_list[m][n])

    book.save(filename)