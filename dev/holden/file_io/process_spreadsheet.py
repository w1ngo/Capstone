import pandas as pd


def read_excel_file(filename: str, sheet: int=0) -> pd.core.frame.DataFrame:
    return pd.read_excel(filename, sheet, index_col = 0)
    # return pd.read_excel(filename)
    #ENDOF: read_excel_file()


def write_excel_file(filename: str, data: pd.core.frame.DataFrame):
    data.to_excel(filename, index=False, header=True)
    #ENDOF: write_excel_file()


def append_excel_file(filename: str, data: list[list]):
    return
    #ENDOF: append_excel_file()


def read_csv(filename: str):
    return
    #ENDOF: read_csv()


def write_csv(filename: str):
    return
    #ENDOF: write_csv()


def append_csv(filename: str):
    return
    #ENDOF: append_csv()


if __name__=="__main__":
    frame = read_excel_file("SPR Gravity 2022.xlsx", "22SPR")
    print(type(frame))
    print(frame)

    write_excel_file("gravity_copy.xlsx", frame)
