import nfl_data_py as nfl



def main() -> str:
    # creating the dataframe to get player name, id and position
    df = nfl.import_seasonal_data(range(2015, 2025),"REG")
    print(df.columns)
    return "SEE"

main()