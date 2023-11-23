import tabula
from tabulate import tabulate
def scrape():
    df = tabula.read_pdf("data/pdf/BSL.pdf", pages=['3','4','5'], multiple_tables=True)
    df2 = tabula.read_pdf("data/pdf/PATCO_Timetable_2023-07-08.pdf", pages='all', multiple_tables=True)
    for frame in df2:
        print(tabulate(frame))
    
    for frame in df:
        print(tabulate(frame))

    text_file=open("output.csv","w")
    for frame in df:
        text_file.write(str(frame))
    text_file.close()
    

  #  tabula.convert_into("data/pdf/BSL.pdf", "output.csv", output_format="csv", pages='3')
    tabula.convert_into("data/pdf/PATCO_Timetable_2023-07-08.pdf", "output2.csv", output_format="csv", pages='2')
    
if __name__ == '__main__':
    scrape()