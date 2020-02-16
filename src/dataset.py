import pandas as pd

from pathlib import Path
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities


def _register_bundle(df, csv_path_to_save, time_column_label=None):
    '''
    args:
        df: dataframe containing the dayly rates
        csv_path_to_save:
        time_column_label = None: name of the column containing the datetime (None for dataframe index)
    '''
    _save_csv(df, csv_path_to_save)

    symbol_name = df.symbol.values[0]
    if time_column_label is None:
        from_datetime = df.index.min()
        to_datetime = df.index.min()
    else:
        from_datetime = df[time_column_label].min()
        to_datetime = df[time_column_label].max()

    register(
        'custom_bundle',
        csvdir_equities(
            ['daily'],
            str(csv_path_to_save),
        ),
        calendar_name=symbol_name,
        start_session=pd.Timestamp(from_datetime),
        end_session=pd.Timestamp(to_datetime)
    )


def _save_csv(g, path_to_save):
    g[["date", "open", "high", "low",
       "close", "volume", "dividend", "split"]]\
        .to_csv(path_to_save / g.symbol.values[0], index=False)


def create_zipline_dataset(df, dividends=0.0, splits=1.0, path_to_save=Path("/usr/lib/site-packages/zipline/data/csvdata/")):
    zipline_rates = df.reset_index().rename(
        columns={"time": "date", "real_volume": "volume"})
    zipline_rates = zipline_rates.assign(dividend=dividends, split=splits)
    zipline_rates.groupby("symbol").apply(
        _register_bundle, args=(path_to_save))
