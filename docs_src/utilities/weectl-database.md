# weectl database

Use the `weectl` subcommand `database` to manage the WeeWX database.

Specify `--help` to see the various actions and options:

    weectl database --help

## Common options

These are options used by most of the actions.

### --config

Path to the configuration file. Default is `~/weewx-data/weewx.conf`.

### --binding

The database binding to use. Default is `wx_binding`.

### --dry-run

Show what would happen if the action was run, but do not actually make any writable changes.

## Create a new database

    weectl database create
        [--config=CONFIG-PATH] [--binding=BINDING] [--dry-run]

This action is used to create a new database by using the specifications in the configuration
file, `weewx.conf`. It is rarely needed, as `weewxd` will do this automatically on startup.

Use the `--help` option to see how to use this action.

```
weectl database create --help
```

## Drop the daily summaries

    weectl database drop-daily
        [--config=CONFIG-PATH] [--binding=BINDING] [--dry-run]

In addition to the regular archive data, every WeeWX database also includes a daily summary table
for each observation type. Because there can be dozens of observation types, there can be dozens of
these daily summaries. It does not happen very often, but there can be occasions when it's
necessary to drop them all and then rebuild them. Dropping them by hand would be very tedious! This
action does them all at once.

Use the `--help` option to see how to use this action:

    weectl database drop-daily --help

## Rebuild the daily summaries

    weectl database rebuild-daily 
        [[--date=YYYY-mm-dd] | [--from=YYYY-mm-dd] [--to=YYYY-mm-dd]] 
        [--config=CONFIG-PATH] [--binding=BINDING] [--dry-run]

This action is the inverse of action `weectk database drop-daily` in that it rebuilds the daily
summaries from the archive data.

The action `rebuild-daily` accepts a number of date related options, `--date`, `--from` and `--to`
that allow selective rebuilding of the daily summaries for one or more days rather than for the
entire archive history. These options may be useful if bogus data has been removed from the archive
covering a single day or a period of few days. The daily summaries can then be rebuilt for this
period only, resulting in a faster rebuild and detailed low/high values and the associated times
being retained for unaffected days.

### Rebuild a specific date

    weectl database rebuild-daily --date=YYYY-mm-dd

Use this form to rebuild the daily summaries for a specific date.

### Rebuild for a range of dates

    weectl database rebuild-daily --from=YYYY-mm-dd --to=YYYY-mm-dd

Use this form to rebuild for an inclusive interval of dates. The default value for `--from` is from
the first day in the database. The default value for `--to` is the last day in the database.

!!! Note

    The period defined by `--to` and `--from` is inclusive.

## Add a new observation type to the database

    weectl database add-column NAME --type=COLUMN-DEF
        [--config=CONFIG-PATH] [--binding=BINDING] [--dry-run]

This action adds a new database observation type (column), given by `NAME`, to the database. The
option `--type` is any valid SQL column definition. It defaults to `REAL`.

For example, to add a new observation `pulseCount` with a SQL type of `INTEGER`, whose default
value is zero:

    weectl database add-column pulseCount --type "INTEGER DEFAULT 0"

## Rename an observation type

    weectl database rename-column FROM-NAME TO-NAME
        [--config=CONFIG-PATH] [--binding=BINDING] [--dry-run]

Use this action to rename a database observation type (column) to a new name.

For example, to rename the column `luminosity` in your database to `illuminance`:

    weectl database rename-column luminosity illuminance

## Drop (remove) observation types

    weectl database drop-columns NAME...
        [--config=CONFIG-PATH] [--binding=BINDING] [--dry-run]

This action will drop one or more observation types (columns) from the database. If more than one
column name is given, they should be separated by spaces.

!!! Note
    
    When dropping columns from a SQLite database, the entire database must be copied except for the
    dropped columns. Because this can be quite slow, if you are dropping more than one column, it is
    better to do them all in one pass. This is why action `drop-columns` accepts more 
    than one name.


## Reconfigure a database

    weectl database reconfigure
        [--config=CONFIG-PATH] [--binding=BINDING] [--dry-run]

This action is useful for changing the schema or unit system in your database.

It creates a new database with the same name as the old, except with the suffix `_new` attached at
the end (nominally, `weewx.sdb_new` if you are using SQLite, `weewx_new` if you are using MySQL).
It then initializes the database with the schema specified in `weewx.conf`. Finally, it copies over
the data from your old database into the new database.

See the section [_Changing the database unit system in an existing
database_](/custom/database/#Changing_the_unit_system) in the _Customization Guide_ for step-by-step
instructions that use this option.

## Transfer (copy) a database

    weectl database transfer --dest-binding=BINDING-NAME
        [--config=CONFIG-PATH] [--binding=BINDING] [--dry-run]

This action is useful for moving your database from one type of database to another, such as from
SQLite to MySQL. To use it, you must have two bindings specified in your `weewx.conf` configuration
file. One will serve as the source, the other as the destination. Specify the source binding with
option `--binding` (default `wx_binding`), the destination binding with option `--dest-binding`
(required).

See the Wiki for examples of moving data from [SQLite to
MySQL](https://github.com/weewx/weewx/wiki/Transfer%20from%20sqlite%20to%20MySQL#using-wee_database),
and from [MySQL to SQLite](https://github.com/weewx/weewx/wiki/Transfer%20from%20MySQL%20to%20sqlite#using-wee_database)
by using `weectl database transfer`.


## Calculate missing derived variables

    weectl database calc-missing
        [--date=YYYY-mm-dd | [--from=YYYY-mm-dd[THH:MM]] [--to=YYYY-mm-dd[THH:MM]]]
        [--config=CONFIG-PATH] [--binding=BINDING-NAME]
        [--dry-run]

This action calculates derived observations for archive records in the database and then stores the
calculated observations in the database. This can be useful if erroneous archive data is corrected
or some additional observational data is added to the archive that may alter previously calculated
or missing derived observations.

The period over which the derived observations are calculated can be limited
through use of the `--date`, `--from` and/or `--to` options. When used without
any of these options `--calc-missing` will calculate derived observations for
all archive records in the database. The `--date` option limits the calculation
of derived observations to the specified date only. The `--from` and `--to`
options can be used together to specify the start and end date-time
respectively of the period over which derived observations will be calculated.

If `--from` is used by itself the period is fom the date-time specified up to
and including the last archive record in the database.

If `--to` is used by itself the period is the first archive record in the
database through to the specified date-time.

```
weectl database calc-missing
weectl database calc-missing --date=YYYY-mm-dd
weectl database calc-missing --from=YYYY-mm-dd[THH:MM]
weectl database calc-missing --to=YYYY-mm-dd[THH:MM]
weectl database calc-missing --from=YYYY-mm-dd[THH:MM] --to=YYYY-mm-dd[THH:MM]
```

!!! Note
    Action `calc-missing` uses the `StdWXCalculate` service to calculate missing
    derived observations. The data binding used by the `StdWXCalculate` service
    should normally match the data binding of the database being operated on by
    `calc-missing`. Those who use custom or additional data bindings should
    take care to ensure the correct data bindings are used by both
    `calc-missing` and the `StdWXCalculate` service.


## Check a database

    weectl database check
        [--config=CONFIG-PATH] [--binding=BINDING-NAME]

Databases created earlier than 3.7.0 (released 11-March-2017) have a flaw that prevents them
from being used with archive intervals that change with time. This utility check whether your
database is affected. See [Issue #61](https://github.com/weewx/weewx/issues/61).

## Update a database

    weectl database update
        [--config=CONFIG-PATH] [--binding=BINDING-NAME]
        [--dry-run]

This action updates the daily summary tables to use interval weighted calculations (see 
[Issue #61](https://github.com/weewx/weewx/issues/61)) as well as recalculating the `windSpeed` maximum
daily values and times (see [Issue #195](https://github.com/weewx/weewx/issues/195)). Interval
weighted calculations are only applied to the daily summaries if not previously applied. The update
process is irreversible and users are advised to back up their database before performing this
action.

For further information on interval weighting and recalculation of daily `windSpeed` maximum
values, see the sections [_Changes to daily summaries_](/versions/#changes-to-daily-summaries) and
[_Recalculation of wind speed maximum values_](/versions/#recalculation-of-windspeed-maximum-values)
in the Upgrade Guide.

## Recalculate daily summary weights

    weectl database reweight
        [[--date=YYYY-mm-dd] | [--from=YYYY-mm-dd] [--to=YYYY-mm-dd]] 
        [--config=CONFIG-PATH] [--binding=BINDING] [--dry-run]

As an alternative to dropping and rebuilding the daily summaries, this action simply rebuilds the
weighted daily sums (used to calculate averages) from the archive data. It does not touch the highs
and lows. It is much faster than `weectl database rebuild-daily`, and has the advantage that the
highs and lows remain unchanged.

Other options are as in `weectl database rebuild-daily`.


