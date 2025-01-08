from data.launaReiknivel.loadData import *
import pathlib

def main():
    workingDir = pathlib.Path(__file__).parent.resolve()
    fileName = f"{str(workingDir)}/data/launaReiknivel/launaReiknivel.xlsx"
    loadData(fileName).openExcelFile()
    


if __name__ == "__main__":
    main()
