TIPS = [
    {
        "id": 1,
        "title": "DataFrame, the spreadsheet of Python",
        "definition": "pd.DataFrame builds a labeled two-dimensional table: rows and columns, each with a name and a dtype. It stores heterogeneous data — numbers, text, dates — in one structure whose operations (filtering, grouping, plotting) are built to match how people actually think about data.",
        "example": "import pandas as pd\ndf = pd.DataFrame({'name': ['Ada', 'Lin'], 'score': [95, 88]})",
        "usecase": "The core object of all pandas work — every CSV, query result or Excel sheet becomes one, and everything else hangs off it.",
        "category": "pandas"
    },
    {
        "id": 2,
        "title": "read_csv is the front door",
        "definition": "pd.read_csv loads a delimited file straight into a DataFrame, with arguments to control parsing: parse_dates promotes date-looking strings to timestamps, usecols trims columns at load time, and dtype pins column types as they arrive. Most data work starts with exactly this one call.",
        "example": "df = pd.read_csv('sales.csv', parse_dates=['date'], dtype={'zip': 'str'})",
        "usecase": "Kicking off 90% of data projects — CSV exports from databases and spreadsheets land as a ready-to-use DataFrame.",
        "category": "pandas"
    },
    {
        "id": 3,
        "title": "head/tail/info/describe in one breath",
        "definition": "A first glance at any DataFrame: head() and tail() peek at the first and last rows, info() lists columns with their dtypes and non-null counts, and describe() summarizes numeric columns with count, mean, min, quartiles and max. Four calls, thirty seconds, full orientation.",
        "example": "df.head(10)\ndf.tail(3)\ndf.info()\ndf.describe()",
        "usecase": "The 30-second orientation to a new dataset — sample rows, types, missing counts and ranges before writing any real code.",
        "category": "pandas"
    },
    {
        "id": 4,
        "title": "dtypes matter, astype fixes them",
        "definition": "Every column carries a dtype that governs how pandas stores and computes with it. Imported data frequently mislabels columns — numbers stored as strings, dates as objects — and astype, to_numeric and to_datetime recast them so comparisons, math and sorting behave correctly.",
        "example": "df['price'] = pd.to_numeric(df['price'], errors='coerce')   # bad entries become NaN",
        "usecase": "Fixing imported columns that look like numbers but behave like text — the first friction point of any real dataset.",
        "category": "pandas"
    },
    {
        "id": 5,
        "title": "picking columns with ease",
        "definition": "df['col'] returns a Series — one named column — while df[['a', 'b']] returns a DataFrame with the chosen subset; attribute access like df.col works for simple names. Selecting the right fields is how you trim data down to what a chart, merge or model actually needs.",
        "example": "names = df['name']\nsubset = df[['name', 'score']]",
        "usecase": "Selecting the fields you need for a chart, a join or a model — the most common single operation in pandas.",
        "category": "pandas"
    },
    {
        "id": 6,
        "title": "loc and iloc, the two selectors",
        "definition": "df.loc selects by label or boolean mask, df.iloc selects by integer position — two different conventions for the same rows. loc follows the actual index values, so it survives sorting and reshuffling; iloc always counts from zero in current row order. Choosing consciously prevents classic off-by-one bugs.",
        "example": "df.loc[2]         # row whose INDEX is 2\ndf.iloc[2]        # third row by position",
        "usecase": "Precise row access after sorting, filtering or reshaping — loc tracks meaning, iloc tracks position.",
        "category": "pandas"
    },
    {
        "id": 7,
        "title": "Boolean masks filter rows",
        "definition": "A condition on a column produces a boolean Series — True where the test passes. Passing that mask back to df[] keeps only the matching rows. It composes with &, | and ~ for compound conditions, giving the most readable way to filter without loops.",
        "example": "adults = df[df['age'] >= 18]\nactive = df[(df['status'] == 'on') & (df['score'] > 50)]",
        "usecase": "Filtering by any rule — age, dates, memberships, scores — in one readable, vectorized line.",
        "category": "pandas"
    },
    {
        "id": 8,
        "title": "query() reads like SQL",
        "definition": "df.query() filters with a string expression using Python comparison and logic operators — 'age >= 18 and city == \"Berlin\"'. Column names are referenced bare, no brackets or masks, so complex conditions read like a WHERE clause instead of nested bracket chains.",
        "example": "df.query('age >= 18 and city == \"Berlin\"')",
        "usecase": "Readable multi-condition filters without stacked bracket-mask chains — SQL-style clarity inside pandas.",
        "category": "pandas"
    },
    {
        "id": 9,
        "title": "sort_values orders the world",
        "definition": "df.sort_values orders rows by one or more columns, ascending or descending, with by= accepting a list for multi-key sorting. Whether ranking scores, ordering by date or building a leaderboard, it rearranges the frame without changing any values in it.",
        "example": "df.sort_values(['city', 'score'], ascending=[True, False])",
        "usecase": "Leaderboards, top-N lists and chronological ordering — the step before most grouping and reporting.",
        "category": "pandas"
    },
    {
        "id": 10,
        "title": "groupby, the heart of analysis",
        "definition": "df.groupby(key) splits the frame into groups sharing the same key value, then aggregates each — sum, mean, count, max, and more — producing one row per group. It is the engine of summary analysis: per-city totals, per-user averages, per-month counts, all in a line or two.",
        "example": "df.groupby('city')['sales'].sum()",
        "usecase": "Per-city totals, per-user averages, per-month counts — instant summaries that drive almost every business report.",
        "category": "pandas"
    },
    {
        "id": 11,
        "title": "agg for multiple statistics at once",
        "definition": "After grouping, agg() applies several aggregate functions in a single pass, producing a table of columns — one per statistic — per group. Specify a list like ['mean', 'count', 'max'] and pandas computes them together, far more efficiently than separate groupby calls.",
        "example": "df.groupby('city')['score'].agg(['mean', 'count', 'max'])",
        "usecase": "Building one summary table with many metrics per group — means, counts, maxima in a single readable call.",
        "category": "pandas"
    },
    {
        "id": 12,
        "title": "apply for custom logic",
        "definition": "df.apply() runs a function across rows (axis=1) or columns (axis=0) when no built-in vector operation fits. It hands each row or column to your function and collects the results — the escape hatch for computations like custom scoring or text cleanup that built-ins can't express.",
        "example": "df['total'] = df.apply(\n    lambda r: r['qty'] * r['price'], axis=1)",
        "usecase": "Custom scoring, text cleanup or any row-wise computation that doesn't have a vectorized counterpart.",
        "category": "pandas"
    },
    {
        "id": 13,
        "title": "New columns are one assignment away",
        "definition": "Assigning to a new key creates a column: df['total'] = df['qty'] * df['price'] adds a computed Series to the frame. Expressions can mix columns, scalars and functions, so derived fields — totals, rates, deltas — appear with a single vectorized assignment.",
        "example": "df['revenue'] = df['qty'] * df['price']\ndf['high'] = df['score'] >= 80",
        "usecase": "Adding computed fields — totals, rates, flags — before saving, plotting or feeding a model.",
        "category": "pandas"
    },
    {
        "id": 14,
        "title": "dropna vs fillna",
        "definition": "dropna removes rows (or columns) containing missing values, while fillna substitutes a value — a scalar, a statistic like the median, or forward-fill from the previous row. Deleting is right when gaps are unrecoverable; filling preserves rows when a plausible value exists.",
        "example": "df = df.dropna(subset=['email'])                       # drop unfixable\ndf['age'] = df['age'].fillna(df['age'].median())        # impute features",
        "usecase": "Cleaning imports — drop rows you can't rescue, impute features you can, before any analysis or model.",
        "category": "pandas"
    },
    {
        "id": 15,
        "title": "drop_duplicates kills repeats",
        "definition": "df.drop_duplicates removes duplicate rows, by default keeping the first occurrence and judging a row by all columns — or by a subset with the subset= argument. Exports and log dumps frequently contain doubled records, and this is the one-line cleanup that fixes them.",
        "example": "df.drop_duplicates(subset=['email'], keep='first', inplace=True)",
        "usecase": "Deduping contact exports, event logs or any import with doubled records — keep one identity per key.",
        "category": "pandas"
    },
    {
        "id": 16,
        "title": "value_counts for distributions",
        "definition": "df['col'].value_counts() counts how many rows fall into each unique value of a column, sorted by frequency — with normalize=True it returns proportions instead. It answers 'what values exist, and how rare is each?' for categories, booleans or any discrete column.",
        "example": "df['status'].value_counts()\ndf['city'].value_counts(normalize=True)",
        "usecase": "Distribution checks — seeing exactly what values exist, their counts and their share, before deciding how to handle them.",
        "category": "pandas"
    },
    {
        "id": 17,
        "title": "unique and nunique, distinct values",
        "definition": "column.unique() returns the distinct values in a column as an array, and column.nunique() counts them. Together they measure cardinality — how many distinct categories exist — which decides whether a column is categorical, needs encoding, or is effectively an identifier.",
        "example": "cities = df['city'].unique()\nn = df['city'].nunique()",
        "usecase": "Knowing how many categories exist before one-hot encoding, grouping, or flagging a column as an ID.",
        "category": "pandas"
    },
    {
        "id": 18,
        "title": "rename labels at will",
        "definition": "df.rename() remaps column or index labels with a dictionary (columns={'old': 'new'}) or a function. It fixes source typos, standardizes headers across merged exports, and even operates in place — a clean way to align names before anything downstream touches them.",
        "example": "df.rename(columns={'naem': 'name', 'scroe': 'score'}, inplace=True)",
        "usecase": "Fixing typos and standardizing headers from different sources so merges and reports share one naming convention.",
        "category": "pandas"
    },
    {
        "id": 19,
        "title": "set_index / reset_index",
        "definition": "set_index promotes a column to become the DataFrame's index, giving fast label-based lookup; reset_index flattens the index back into a regular column with a fresh RangeIndex. Switching between them toggles whether your keys can be used for loc, joins or time resampling.",
        "example": "df.set_index('id', inplace=True)\nval = df.loc[user_id]\ndf.reset_index(inplace=True)",
        "usecase": "Enabling label-based lookup, index joins, or time-series resampling — then restoring a plain column layout for export.",
        "category": "pandas"
    },
    {
        "id": 20,
        "title": "merge joins tables (SQL join, in pandas)",
        "definition": "pd.merge combines two DataFrames on a key column with SQL semantics: how='inner', 'left', 'right' or 'outer' controls which rows survive, and on= names the shared key. It's the pandas counterpart of a database join, bringing related tables — users and orders, posts and comments — together.",
        "example": "pd.merge(users, orders, on='user_id', how='left')",
        "usecase": "Users plus their orders, posts plus their comments — assembling relational data into one analysis-ready frame.",
        "category": "pandas"
    },
    {
        "id": 21,
        "title": "concat stacks frames",
        "definition": "pd.concat joins multiple DataFrames along axis=0 (rows stacked on rows) or axis=1 (columns side by side), with ignore_index=True renumbering rows as one clean sequence. It is the tool for append-style assembly — monthly exports, survey batches, split files — where tables share columns.",
        "example": "all_data = pd.concat([jan, feb, mar], ignore_index=True)",
        "usecase": "Combining monthly exports or appending survey batches into one table — same columns, stacked end to end.",
        "category": "pandas"
    },
    {
        "id": 22,
        "title": "pivot_table, Excel in pandas",
        "definition": "pd.pivot_table builds a cross-tabulated summary: one or more grouping columns become the index, another becomes the columns, and an aggfunc computes values per intersection — the pandas equivalent of an Excel pivot. Aggregations like sum, mean or count turn long data into a report grid.",
        "example": "pd.pivot_table(df, values='sales', index='city',\n                columns='year', aggfunc='sum')",
        "usecase": "City-by-year sales matrices and similar cross-tabulation reports — the classic summary shape for stakeholders.",
        "category": "pandas"
    },
    {
        "id": 23,
        "title": "melt reshapes wide to long",
        "definition": "pd.melt unpivots several value columns into two: one holding the former column names (variable) and one their values — the exact inverse of pivot_table. Long form is what plotting libraries and tidy-data workflows expect: one row per observation, ready to facet by the melted key.",
        "example": "tidy = df.melt(id_vars=['city'], value_vars=['2024', '2025'],\n               var_name='year', value_name='sales')",
        "usecase": "Preparing wide reports for plotting libraries that expect one row per point — the canonical wide-to-long reshape.",
        "category": "pandas"
    },
    {
        "id": 24,
        "title": "to_datetime unlocks time logic",
        "definition": "pd.to_datetime converts date-like strings (and integers, epochs, existing objects) into proper timestamps. Once a column is datetime it can be sorted chronologically, sliced by date ranges, grouped by month, resampled and differenced — none of which behaves sensibly on text.",
        "example": "df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')",
        "usecase": "Turning text dates into real time — the first, mandatory step of any time-series or date-driven analysis.",
        "category": "pandas"
    },
    {
        "id": 25,
        "title": "resample, time buckets made easy",
        "definition": "With a DatetimeIndex, resample() rebuckets data into coarser time periods — daily, weekly, monthly — then aggregates each bucket with a function like sum or mean. Milliseconds of event logs become a clean daily or weekly dashboard line, nothing hand-grouped.",
        "example": "daily = df.set_index('date').resample('D').sum()\nweekly = df.set_index('date').resample('W').mean()",
        "usecase": "Aggregating granular events into daily, weekly or monthly summaries for schedules, dashboards and reports.",
        "category": "pandas"
    },
    {
        "id": 26,
        "title": "rolling windows smooth series",
        "definition": "column.rolling(window).mean() (or sum, std, min…) computes the statistic over a sliding window of the previous N rows at every position. Rolling averages iron out noise and reveal the underlying trend — the standard smoothing tool for noisy time series.",
        "example": "df['ma7'] = df['sales'].rolling(7).mean()\ndf['vol'] = df['sales'].rolling(30).std()",
        "usecase": "Seven-day moving averages to see the trend through weekly noise, or rolling volatility for financial series.",
        "category": "pandas"
    },
    {
        "id": 27,
        "title": ".str accessor for text columns",
        "definition": "column.str exposes string methods directly on a Series of text: lower, strip, contains, startswith, split, replace, extract and more. What would be a Python loop becomes a vectorized cascade of string ops applied to every cell at once.",
        "example": "df['clean_email'] = df['email'].str.strip().str.lower()\ndf['domain'] = df['email'].str.split('@').str[1]",
        "usecase": "Normalizing emails, URLs and product names, or extracting pieces of text — before dedup, matching or reporting.",
        "category": "pandas"
    },
    {
        "id": 28,
        "title": "categorical dtype saves memory",
        "definition": "Casting a column with few unique values to the categorical dtype stores each distinct value once and keeps only an integer code per row — a huge memory saving on big frames with repeated strings. It also accelerates groupby and preserves an ordered category list if supplied.",
        "example": "df['city'] = df['city'].astype('category')\nprint(df['city'].cat.codes)",
        "usecase": "Columns with low cardinality — country, status, product type — in large frames can cut memory use by an order of magnitude.",
        "category": "pandas"
    },
    {
        "id": 29,
        "title": "shift for lagged columns",
        "definition": "column.shift(n) moves values down (positive n) or up (negative n), yielding the previous or next row's value for each position. A lagged column lets each row see its own past — the raw material of day-over-day change and time-series features.",
        "example": "df['prev_day'] = df['sales'].shift(1)\ndf['change'] = df['sales'] - df['prev_day']",
        "usecase": "Day-over-day deltas and lagged features for forecasting — each row learns to predict from its own history.",
        "category": "pandas"
    },
    {
        "id": 30,
        "title": "nlargest / nsmallest, top lists",
        "definition": "df.nlargest(n, 'col') returns the n rows with the highest values in that column, and nsmallest the lowest — without sorting the entire frame first. For top-N questions like leaderboards and best-performers it is both faster and more readable than a full sort plus head.",
        "example": "df.nlargest(10, 'sales')\ndf.nsmallest(5, 'age')",
        "usecase": "Top customers, best products, highest scorers — instant top lists on large frames without a full sort.",
        "category": "pandas"
    },
    {
        "id": 31,
        "title": "sample for randomness",
        "definition": "df.sample(n) pulls random rows — with frac= a random fraction, random_state= for reproducibility and weights= for biased draws. It is the fastest way to eyeball a huge frame, build a quick random subset, or simulate a bootstrapped resample.",
        "example": "df.sample(1000, random_state=42)\ndf.sample(frac=0.1)",
        "usecase": "Spot-checking a million-row frame or building a quick random train/test split before heavy analysis.",
        "category": "pandas"
    },
    {
        "id": 32,
        "title": "map transforms values",
        "definition": "column.map() passes each value through a dict or function and replaces it with the result — perfect for recoding codes to labels, bucketing values, or applying a scalar transformation column-wide. Unlike apply on rows, it works on a single Series's values.",
        "example": "df['grade'] = df['score'].map(\n    lambda s: 'A' if s >= 90 else ('B' if s >= 80 else 'C'))",
        "usecase": "Recoding status codes to readable labels, bucketing values into grades, or applying a function to one column.",
        "category": "pandas"
    },
    {
        "id": 33,
        "title": "explode flattens list cells",
        "definition": "df.explode('col') takes rows whose cell holds a list and emits one row per element, repeating the other columns. It is the inverse of grouping several values into one cell — tags, categories or multi-values become normal, joinable rows for analysis.",
        "example": "df.explode('tags')   # rows with [a, b] become two rows",
        "usecase": "Tags, categories or multi-valued cells spread into regular rows — ready for grouping, pivoting or counting.",
        "category": "pandas"
    },
    {
        "id": 34,
        "title": "crosstab, quick contingency tables",
        "definition": "pd.crosstab(index, columns) tallies the co-occurrence of two columns into a frequency matrix: rows for the first variable, columns for the second, counts in every cell. With values+aggfunc it computes sums or means instead of counts — the fastest contingency table in pandas.",
        "example": "pd.crosstab(df['city'], df['category'])\npd.crosstab(df['city'], df['category'], values=df['sales'], aggfunc='sum')",
        "usecase": "City-by-category distribution counts, or cross-tabulated sums — instant two-dimensional frequency reports.",
        "category": "pandas"
    },
    {
        "id": 35,
        "title": "merge with on vs left_on/right_on",
        "definition": "When both frames name the join key identically, on='key' suffices; when they differ, left_on='uid' and right_on='user_id' tell each side which column to match. Explicitly naming both sides keeps merges unambiguous across sources that use different conventions.",
        "example": "pd.merge(users, orders, left_on='uid', right_on='user_id')",
        "usecase": "Joining tables whose key columns are named differently across sources — the common case when merging vendor data.",
        "category": "pandas"
    },
    {
        "id": 36,
        "title": "to_csv, export everything back",
        "definition": "df.to_csv writes the frame to a delimited file — index=False drops the row index, compression='gzip' shrinks big exports, and header/columns control the output columns. It is the mirror of read_csv, producing files any tool, service or person can open.",
        "example": "df.to_csv('out.csv', index=False)\ndf.to_csv('out.csv.gz', compression='gzip')",
        "usecase": "Sharing results with non-Python tooling, saving processed data, or producing a deliverable export for stakeholders.",
        "category": "pandas"
    },
    {
        "id": 37,
        "title": "datetime components via .dt",
        "definition": "For a datetime Series, .dt exposes the components: .dt.year, .dt.month, .dt.weekday, .dt.day_name(), .dt.hour and more. Extracting these parts turns one timestamp column into several discrete-feature columns for seasonality analysis or grouping.",
        "example": "df['year'] = df['date'].dt.year\ndf['dow'] = df['date'].dt.day_name()\ndf['hour'] = df['date'].dt.hour",
        "usecase": "Seasonality analysis, monthly breakdowns or weekday grouping — decomposing timestamps into analyzable parts.",
        "category": "pandas"
    },
    {
        "id": 38,
        "title": "pipe chains functions reading",
        "definition": "df.pipe(f) passes the frame to a function and returns its result — and chains compose: df.pipe(clean).pipe(fill_gaps).pipe(add_totals) reads top to bottom like a recipe. Each step takes the DataFrame, returns a DataFrame, and the code reads in the order it executes.",
        "example": "result = (df.pipe(clean_columns)\n            .pipe(impute_missing)\n            .pipe(add_totals))",
        "usecase": "Readable, sequential transformation pipelines instead of nested function calls — clarity in the order data flows.",
        "category": "pandas"
    },
    {
        "id": 39,
        "title": "vectorized beats loops every time",
        "definition": "Pandas operations act on whole columns in compiled code; looping row by row with iterrows() interleaves slow Python per row. A vectorized expression like df['total'] = df['qty'] * df['price'] computes every value at once — often orders of magnitude faster on real-sized frames.",
        "example": "df['total'] = df['qty'] * df['price']   # vectorized, no loop",
        "usecase": "Any computation over big frames — vectorize and watch minutes of row-loops shrink to milliseconds.",
        "category": "pandas"
    },
    {
        "id": 40,
        "title": "applymap for whole-frame transforms",
        "definition": "df.applymap(f) applies a function to every single cell of a DataFrame — cleaning whitespace, coercing text, or formatting values across all cells at once. It is elementwise across the entire frame, distinct from apply which works per row or column.",
        "example": "df = df.applymap(lambda x: str(x).strip())",
        "usecase": "Stripping whitespace or normalizing every text cell at once — a one-call pass over the whole table.",
        "category": "pandas"
    },
    {
        "id": 41,
        "title": "NaN handling, the friendly ways",
        "definition": "pandas offers several missing-value strategies: dropna removes rows with gaps, fillna substitutes a fixed value or statistic, interpolate fills by interpolation between neighbors, and filling methods like ffill carry the last known value forward. Each fits a different kind of gap, and choosing is a data decision.",
        "example": "df = df.dropna(subset=['email'])         # drop unfixable rows\ndf['sales'] = df['sales'].interpolate()    # fill curves smoothly\ndf['status'] = df['status'].fillna(method='ffill')",
        "usecase": "Time series with missing readings get interpolated to stay continuous; sparse columns get a sensible fill or dropped rows — handled gracefully per column.",
        "category": "pandas"
    },
    {
        "id": 42,
        "title": "cut vs qcut, binning two ways",
        "definition": "pd.cut divides a numeric column into equal-width bins by value ranges you specify; pd.qcut divides into equal-size bins by rank, each containing the same number of rows. Width matters for ranges like age brackets; count matters for quartiles on skewed scores.",
        "example": "pd.cut(df['age'], bins=[0, 18, 35, 65], labels=['young', 'adult', 'senior'])\npd.qcut(df['score'], q=4)",
        "usecase": "Age brackets defined by meaningful ranges versus quartile groups that balance each bucket — pick the binning that matches the question.",
        "category": "pandas"
    },
    {
        "id": 43,
        "title": "clip clamps values",
        "definition": "column.clip(lower, upper) caps every value into a range, replacing anything below with lower and above with upper — without deleting rows. It tames outlier typos and implements winsorizing-style bounds on a column in a single call, preserving every observation.",
        "example": "df['salary'] = df['salary'].clip(upper=200_000)   # cap outliers",
        "usecase": "Neutralizing data-entry typos or bounding extremes before statistics — outliers get clamped instead of skewing every aggregate.",
        "category": "pandas"
    },
    {
        "id": 44,
        "title": "duplicated marks repeat rows",
        "definition": "df.duplicated() returns a boolean Series flagging rows that repeat an earlier row — by all columns by default, or by a subset with the subset= argument. Combined with boolean masking it both selects the duplicates for inspection and powers the keep logic before dropping.",
        "example": "mask = df.duplicated(subset=['email'], keep=False)\nduplicates = df[mask]        # every copy, first one included",
        "usecase": "Finding every duplicate contact before deciding which to keep — visibility first, deletion second.",
        "category": "pandas"
    },
    {
        "id": 45,
        "title": "astype to category, then factorize",
        "definition": "pd.factorize(column) encodes categorical strings into integer codes ready for machine-learning models, returning both the codes and the unique values in order. Combined with astype('category'), it turns labels into the compact integer representation models actually ingest.",
        "example": "codes, uniques = pd.factorize(df['city'])\ndf['city_code'] = codes",
        "usecase": "Converting categorical strings into numeric codes before feeding a classifier — the last step from text to model-ready columns.",
        "category": "pandas"
    },
    {
        "id": 46,
        "title": "inplace=True or reassign, pick one",
        "definition": "Most pandas operations return a new DataFrame, leaving the original untouched; inplace=True instead mutates the object directly. Mutation risks surprising aliases when a frame is shared, so reassigning the result (df = df.dropna()) is the safer, more predictable habit.",
        "example": "df = df.dropna()          # new frame, original untouched\n# versus\n df.dropna(inplace=True)  # mutates the object",
        "usecase": "Avoiding surprises in chained or shared-frame code — explicit reassignment keeps every step visible and side-effect free.",
        "category": "pandas"
    },
    {
        "id": 47,
        "title": "Group keys stay in the result",
        "definition": "groupby moves the grouping columns into the result's index, which is efficient but sometimes inconvenient. reset_index() demotes that index back into ordinary columns, producing a flat table of grouped results ready for merging or direct export.",
        "example": "summary = (df.groupby('city')['sales']\n             .sum().reset_index())",
        "usecase": "Getting a flat, mergeable table of grouped outcomes — the shape charts and exports expect after any grouping.",
        "category": "pandas"
    },
    {
        "id": 48,
        "title": "Memory, memory, memory",
        "definition": "Big frames shrink dramatically when you read only what you need: usecols trims columns, dtype pins small ints and strings, and low_memory/parse_dates balance speed. Downcasting numerics and categorical columns finish the job — together they turn RAM-heavy imports into manageable ones.",
        "example": "df = pd.read_csv(\n    'big.csv',\n    dtype={'zip': 'int32', 'status': 'category'},\n    usecols=['zip', 'status', 'sales'])",
        "usecase": "Handling datasets that barely fit in RAM — trimming columns, tightening dtypes and using categories until the frame fits comfortably.",
        "category": "pandas"
    },
    {
        "id": 49,
        "title": "Merging on indexes, clean joins",
        "definition": "When the join keys live in the index rather than regular columns, pd.merge accepts left_index=True and right_index=True to join on them directly — no reset_index choreography. Index joins are fast lookups and keep multi-level indexes working as the merge key.",
        "example": "pd.merge(sales, targets, left_index=True, right_index=True)",
        "usecase": "Joining pre-indexed frames — aligning daily series or category tables whose keys are already the index.",
        "category": "pandas"
    },
    {
        "id": 50,
        "title": "Data validation starts with shape",
        "definition": "A quick audit before trusting any result: df.shape reports rows and columns, df.dtypes reveals mis-parsed types, and df.isna().sum() counts missing values per column. Three calls catch the majority of import problems and keep you from decoding errors on bad assumptions.",
        "example": "print(df.shape)\nprint(df.dtypes)\nprint(df.isna().sum().sort_values(ascending=False))",
        "usecase": "The discipline of checking the frame before trusting any number from it — a two-second habit that prevents costly misinterpretation.",
        "category": "pandas"
    }
]
