
from pathlib import Path
import pytz

MAGIC_ZIPLINE_FILE_TO_ADD_BUNDLES = "C:/Python36/Lib/site-packages/zipline/extensions.py"
IMPORTS_IN_MAGIC_ZIPLINE_FILE_TO_ADD_BUNDLES =\
    "from zipline.data.bundles.csvdir import csvdir_equities\n"\
    "from zipline.data.bundles import register\n"\
    "import pandas as pd"


def _register_bundle(df, csv_path_to_save, tz, file_handle):
    '''
    args:
        df: dataframe containing the dayly rates
        csv_path_to_save:
    '''
    _save_csv(df, csv_path_to_save)

    symbol_name = df.symbol.values[0]

    from_datetime = df["date"].min()
    to_datetime = df["date"].max()

    file_handle.write(
        "\nregister(\"custom_bundle\", csvdir_equities(['daily'], \"%s\"),"
        "calendar_name=\"%s\", start_session=pd.Timestamp(\"%s\", tz=pytz.timezone(\"%s\")),"
        "end_session=pd.Timestamp(\"%s\", tz=pytz.timezone(\"%s\")))" % (
            str(csv_path_to_save), symbol_name, str(from_datetime), str(tz), str(to_datetime), str(tz))
    )


def _save_csv(g, path_to_save):
    g[["date", "open", "high", "low",
       "close", "volume", "dividend", "split"]]\
        .to_csv(path_to_save / g.symbol.values[0], index=False)


def create_zipline_dataset(
        df, dividends=0.0, splits=1.0,
        path_to_save=Path("/usr/lib/site-packages/zipline/data/csvdata/"),
        tz=pytz.timezone('Brazil/East')):

    zipline_rates = df.reset_index().rename(
        columns={"time": "date", "real_volume": "volume"})
    zipline_rates = zipline_rates.assign(dividend=dividends, split=splits)

    with open(MAGIC_ZIPLINE_FILE_TO_ADD_BUNDLES, 'a') as file_handle:
        file_handle.write(IMPORTS_IN_MAGIC_ZIPLINE_FILE_TO_ADD_BUNDLES)
        [_register_bundle(group, path_to_save, tz, file_handle)
         for _key, group in zipline_rates.groupby("symbol")]
