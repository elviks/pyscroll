TIPS = [
    {
        "id": 1,
        "title": "Streamlit runs the whole script top to bottom",
        "definition": "The defining model of Streamlit: every interaction reruns your entire script from the top. Widgets remember their values across reruns, plain variables reset, and anything you want to persist across reruns must live in st.session_state. Understanding this execution model — pure top-down script, rerun on every event — unlocks everything else in the framework.",
        "example": "# app.py\nimport streamlit as st\n\nst.title(\"My App\")\ncount = 0                      # resets on every rerun\nif st.button(\"Click me\"):\n    count += 1                 # value is lost immediately\nst.write(\"Count:\", count)",
        "usecase": "Recognizing why naive state variables disappear and why expensive queries run again on every click — the mental model every Streamlit feature builds on.",
        "category": "streamlit"
    },
    {
        "id": 2,
        "title": "st.session_state survives reruns",
        "definition": "st.session_state is a persistent per-session dict that survives script reruns: values you store there — counters, selections, computed data — stay available on the next rerun, unlike ordinary variables. Initialize lazily with st.session_state.setdefault(key, default) or the ``if key not in`` guard to make state idempotent under the rerun model.",
        "example": "import streamlit as st\n\nif \"count\" not in st.session_state:\n    st.session_state.count = 0\n\nif st.button(\"+\"):\n    st.session_state.count += 1\n\nst.write(\"Count:\", st.session_state.count)   # survives reruns",
        "usecase": "Persisting counters, selected rows, navigation steps and user progress across widget interactions in any app with state that outlives a single rerun.",
        "category": "streamlit"
    },
    {
        "id": 3,
        "title": "st.write displays almost anything",
        "definition": "st.write is the universal output function: pass strings, numbers, DataFrames, dicts, lists, even matplotlib figures or Altair charts, and Streamlit picks the right rendering. It's the fastest way to inspect data while building, and a pragmatic fallback for mixed content in production apps.",
        "example": "import streamlit as st\nimport pandas as pd\n\ndf = pd.DataFrame({\"a\": [1, 2], \"b\": [3, 4]})\nst.write(\"Hello\", 42, {\"key\": \"value\"}, df)   # all rendered correctly",
        "usecase": "Quick prototyping and mixed-output panels — a caption, a metric and a table on one screen — without choosing a specific widget for every element.",
        "category": "streamlit"
    },
    {
        "id": 4,
        "title": "Magic commands print without st.write",
        "definition": "Any bare expression on its own line in a Streamlit script is 'magic': the value gets displayed automatically as if wrapped in st.write. It works for strings, numbers, dataframes and any st.write-compatible object, letting you sketch an app in near-pure Python with almost no Streamlit calls at all.",
        "example": "import streamlit as st\nimport pandas as pd\n\n\"Hello world\"                     # displayed as markdown\npd.DataFrame({\"x\": [1, 2]})       # displayed as a table",
        "usecase": "Building quick internal dashboards and data exploration scripts where the markup noise of explicit st.write calls would slow down iteration.",
        "category": "streamlit"
    },
    {
        "id": 5,
        "title": "st.title and friends structure the page",
        "definition": "st.title, st.header, st.subheader and st.caption create the text hierarchy of a page, mirroring HTML heading semantics. Combined with st.divider, they give an app a clear narrative — section headers that users can skim, captions that annotate charts. They're the skeleton that layout containers fill in.",
        "example": "import streamlit as st\n\nst.title(\"Sales Dashboard\")\nst.header(\"Revenue\")\nst.subheader(\"Monthly breakdown\")\nst.caption(\"Source: internal CRM export, refreshed daily\")\nst.divider()",
        "usecase": "Organizing any multi-section dashboard so users can scan, understand and trust the structure — the visual skeleton of a polished internal tool.",
        "category": "streamlit"
    },
    {
        "id": 6,
        "title": "st.markdown renders rich text",
        "definition": "st.markdown renders GitHub-flavored markdown — headings, bold, lists, links, even embedded HTML when unsafe_allow_html=True. It's the general-purpose text widget for anything beyond a plain string: documentation panels, formatted reports, inline images. For math, pair it with st.latex or inline $...$ delimiters.",
        "example": "import streamlit as st\n\nst.markdown(\"\"\"\n## Overview\n- **Fast**: built on a rerun model\n- *Simple*: pure Python\n[Docs](https://docs.streamlit.io)\n\"\"\")",
        "usecase": "Authoring rich help sections, feature lists and report intros inside data apps without pulling in a separate frontend framework.",
        "category": "streamlit"
    },
    {
        "id": 7,
        "title": "st.latex renders math formulas",
        "definition": "st.latex renders LaTeX math expressions with the built-in MathJax renderer, and $...$ delimiters inside st.markdown produce inline math. It's the natural fit for scientific and financial dashboards that need formulas — integrals, distributions, equations — rendered crisply without an image pipeline.",
        "example": "import streamlit as st\n\nst.latex(r\"E = mc^2\")\nst.markdown(r\"The mean is $\\mu = \\frac{1}{N}\\sum x_i$\")",
        "usecase": "Documenting the math behind metrics — regression formulas, error bounds, financial rates — directly in the app where the numbers appear.",
        "category": "streamlit"
    },
    {
        "id": 8,
        "title": "st.code shows syntax-highlighted snippets",
        "definition": "st.code displays a code block with syntax highlighting and line numbers (line_numbers=True), taking a language for highlighting — python, sql, bash, json and more. Unlike st.text, the content is never interpreted as markdown, making it the safe choice for showing raw code or log output.",
        "example": "import streamlit as st\n\nst.code(\"\"\"\nSELECT region, SUM(revenue)\nFROM sales\nGROUP BY region\n\"\"\", language=\"sql\", line_numbers=True)",
        "usecase": "Showing setup instructions, SQL the app generated, or Python snippets in docs-style internal tools where highlighting and exactness matter.",
        "category": "streamlit"
    },
    {
        "id": 9,
        "title": "st.sidebar gives every widget a home",
        "definition": "st.sidebar is a container: prefix any element with st.sidebar to render it in the collapsible left panel — controls live there, content stays in the main area. Filters, navigation and settings in the sidebar keep the main view uncluttered and are always visible while users interact with the data.",
        "example": "import streamlit as st\n\nregion = st.sidebar.selectbox(\"Region\", [\"US\", \"EU\", \"APAC\"])\nmetric = st.sidebar.radio(\"Metric\", [\"Revenue\", \"Users\"])\n\nst.title(f\"{metric} by {region}\")\nst.line_chart([1, 3, 2, 4])   # main area stays clean",
        "usecase": "Standard pattern for filter-heavy dashboards: every selector in the sidebar, the chart and table canvas untouched in the main column.",
        "category": "streamlit"
    },
    {
        "id": 10,
        "title": "st.columns splits the layout",
        "definition": "st.columns([2, 1]) creates a list of equally or proportionally sized columns you can write into with context managers: with col1: st.metric(...). Columns lay content side by side — metric cards, charts, side-by-side tables — with widths declared in the list.",
        "example": "import streamlit as st\n\ncol1, col2, col3 = st.columns(3)\nwith col1:\n    st.metric(\"Revenue\", \"$12k\")\nwith col2:\n    st.metric(\"Users\", 420)\nwith col3:\n    st.metric(\"Churn\", \"3.1%\")\n\nwide, narrow = st.columns([3, 1])\nwide.line_chart([1, 4, 2])\nnarrow.write(\"Legend and notes\")",
        "usecase": "Dashboard rows of KPIs and asymmetric layouts — a big chart next to a narrow control column — without touching CSS or HTML.",
        "category": "streamlit"
    },
    {
        "id": 11,
        "title": "st.expander hides details until clicked",
        "definition": "st.expander creates a collapsible section that renders children lazily — the content stays in the DOM but collapses to a single label row, reducing visual noise for secondary information: methodology notes, raw data tables, debug output.",
        "example": "import streamlit as st\n\nst.metric(\"Revenue\", \"$12k\")\nwith st.expander(\"Methodology\"):\n    st.markdown(\"Revenue is net of refunds, in USD, weekly.\")\nwith st.expander(\"Raw data\"):\n    st.dataframe(data)   # hidden until expanded",
        "usecase": "Decluttering dashboards — raw SQL, data dictionaries and caveats go behind expanders, keeping the primary view focused on the numbers.",
        "category": "streamlit"
    },
    {
        "id": 12,
        "title": "st.tabs splits content into tabbed panes",
        "definition": "st.tabs creates named tab panes you write into with context managers. Each tab's content reruns on every script run — like everything in Streamlit — but tabs group related views: separate tabs for summary, detail and settings, or one per chart type.",
        "example": "import streamlit as st\n\ntab1, tab2 = st.tabs([\"Overview\", \"Detail\"])\nwith tab1:\n    st.metric(\"Total\", 100)\nwith tab2:\n    st.dataframe(detail_df)",
        "usecase": "Organizing dense reports — summary view, per-region detail, config panel — so users switch views without scrolling a long single column.",
        "category": "streamlit"
    },
    {
        "id": 13,
        "title": "st.container groups related elements",
        "definition": "st.container returns a block you can write into and use as a target for st.empty placeholders; with st.container(): creates a grouping boundary in the DOM. Containers matter most for ordering and for holding dynamic content — you can clear and refill a container while keeping surrounding elements stable.",
        "example": "import streamlit as st\n\nwith st.container():\n    st.subheader(\"Top region\")\n    st.bar_chart(data)\n\nplaceholder = st.container()\nwith placeholder:\n    st.info(\"Loading...\")\n# later in the same script:\nplaceholder.empty()\nwith placeholder:\n    st.success(\"Done\")",
        "usecase": "Dynamic panels that update in place — loading states, progress sections, refreshable regions — while the rest of the page stays put.",
        "category": "streamlit"
    },
    {
        "id": 14,
        "title": "st.empty creates update-in-place placeholders",
        "definition": "st.empty() reserves a slot that you can replace with .empty(), .text(), .image(), .chart() etc. — the slot updates in place instead of stacking new elements on every rerun. Pair it with a progress loop or polling loop to animate a single region while the rest of the page is static.",
        "example": "import streamlit as st\nimport time\n\nstatus = st.empty()\nfor pct in range(0, 101, 25):\n    status.progress(pct, text=f\"Processing {pct}%\")\n    time.sleep(0.3)\nstatus.success(\"Done\")",
        "usecase": "Live progress bars, rotating status text and regions that refresh on a timer without appending duplicate widgets on each update.",
        "category": "streamlit"
    },
    {
        "id": 15,
        "title": "st.button triggers actions",
        "definition": "st.button returns True for exactly the rerun where it was clicked, making it the natural 'do it now' trigger. Since a click reruns the script, guard the action with if st.button(\"Run\"): to avoid running work before the user asks. Buttons can be configured with type and key.",
        "example": "import streamlit as st\n\nif st.button(\"Run analysis\", type=\"primary\"):\n    result = run_analysis()   # only on click\n    st.write(result)\nelse:\n    st.caption(\"Press the button to start\")",
        "usecase": "Explicit-run workflows — training jobs, report generation, expensive refreshes — where work must wait for a deliberate user action.",
        "category": "streamlit"
    },
    {
        "id": 16,
        "title": "st.text_input captures free text",
        "definition": "st.text_input renders a single-line text field whose current value is returned on every rerun. Combined with an if value: guard it's the standard filter/search widget; type=\"password\" masks the input for API keys and credentials without storing them in session state by default.",
        "example": "import streamlit as st\n\nname = st.text_input(\"Your name\", placeholder=\"Ada Lovelace\")\nkey = st.text_input(\"API key\", type=\"password\")\n\nif name:\n    st.write(f\"Hello, {name}!\")\nif st.button(\"Save key\"):\n    st.session_state.key = key",
        "usecase": "Search boxes, name fields, connection strings and password entry in any form-driven or filter-driven Streamlit app.",
        "category": "streamlit"
    },
    {
        "id": 17,
        "title": "st.number_input for typed numbers",
        "definition": "st.number_input gives a validated numeric field with min_value, max_value, step and value defaults, returning an int or float depending on step. It rejects non-numeric input by construction, saving you from parsing and validating strings — ideal for parameters like thresholds, limits and amounts.",
        "example": "import streamlit as st\n\nage = st.number_input(\"Min age\", min_value=0, max_value=120, value=18, step=1)\nlimit = st.number_input(\"Amount\", min_value=0.0, value=100.0, step=0.5)\n\nst.write(f\"Showing users >= {age} with limit {limit}\")",
        "usecase": "Parameter panels for thresholds and budgets where invalid numbers should be impossible to enter, not caught later in validation code.",
        "category": "streamlit"
    },
    {
        "id": 18,
        "title": "st.slider for ranges and single values",
        "definition": "st.slider returns one value (or a (min, max) tuple when you pass a tuple as value) selected by dragging — natural for interactive filtering. It accepts int, float and even date/datetime ranges, making time-window selectors a single widget rather than two date pickers.",
        "example": "import streamlit as st\n\nscore = st.slider(\"Min score\", 0, 100, 50)\nlo, hi = st.slider(\"Year range\", 2000, 2026, (2015, 2025))\n\nst.write(f\"Score >= {score}, years {lo}-{hi}\")",
        "usecase": "Quick interactive filtering of charts and tables — quality thresholds, time windows, budget bands — with immediate visual feedback.",
        "category": "streamlit"
    },
    {
        "id": 19,
        "title": "st.selectbox for one choice from many",
        "definition": "st.selectbox renders a dropdown returning the chosen item on every rerun; pass any iterable and optional index= for the default selection. For large option lists pass options as a list of dicts or a DataFrame column to keep labels readable, and use format_func to map objects to display text.",
        "example": "import streamlit as st\n\nregion = st.selectbox(\"Region\", [\"US\", \"EU\", \"APAC\", \"LatAm\"], index=1)\n\ndf = load_data()\nproduct = st.selectbox(\"Product\", df[\"name\"].tolist())\nst.write(f\"{region} / {product}\")",
        "usecase": "Dimension pickers in dashboards — region, product line, report type — the canonical widget for switching the slice of data being viewed.",
        "category": "streamlit"
    },
    {
        "id": 20,
        "title": "st.multiselect for zero or more options",
        "definition": "st.multiselect returns a list of all selected options — possibly empty — and is the canonical way to build OR-style filters over categories. Use default=[...] to preselect, and note the empty selection means 'no filter' unless you decide otherwise.",
        "example": "import streamlit as st\n\ncats = st.multiselect(\"Categories\", [\"A\", \"B\", \"C\"], default=[\"A\", \"B\"])\n\nfiltered = df[df[\"cat\"].isin(cats)] if cats else df\nst.dataframe(filtered)",
        "usecase": "Filtering dashboards by any combination of tags, regions or statuses — with empty selection gracefully falling back to all data.",
        "category": "streamlit"
    },
    {
        "id": 21,
        "title": "st.radio for exclusive choices",
        "definition": "st.radio renders mutually exclusive options as clickable pills or list items — returning exactly one value, like selectbox but with every option visible without a dropdown click. It's the right widget when the option set is small and the user should see all choices at a glance.",
        "example": "import streamlit as st\n\nview = st.radio(\"View\", [\"Revenue\", \"Users\", \"Churn\"], horizontal=True)\n\nif view == \"Revenue\":\n    st.line_chart(revenue_series)\nelif view == \"Users\":\n    st.line_chart(users_series)",
        "usecase": "Metric switchers, chart type toggles and small option sets where showing all choices instantly beats a collapsed dropdown.",
        "category": "streamlit"
    },
    {
        "id": 22,
        "title": "st.checkbox for boolean toggles",
        "definition": "st.checkbox returns True or False, ideal for optional features: log raw data, show outliers, enable dark mode for charts. It's the lightest possible interaction — no button click required — and pairs naturally with conditional rendering.",
        "example": "import streamlit as st\n\nshow_outliers = st.checkbox(\"Show outliers\", value=True)\nlog_scale = st.checkbox(\"Log scale\")\n\nst.line_chart(df)\nif show_outliers:\n    st.dataframe(df[df[\"value\"] > 3 * df[\"value\"].std()])",
        "usecase": "Optional behaviors in dashboards — extra tables, annotation layers, debug panes — that appear only when the user asks for them.",
        "category": "streamlit"
    },
    {
        "id": 23,
        "title": "st.date_input for calendar pickers",
        "definition": "st.date_input returns a datetime.date (or a tuple when passed a range tuple as value) picked from a calendar. Combined with min_value/max_value constraints it replaces two text fields for start/end dates, producing real date objects ready for pandas filtering and SQL queries.",
        "example": "import streamlit as st\nfrom datetime import date\n\nstart, end = st.date_input(\"Period\", value=(date(2026, 1, 1), date(2026, 6, 30)))\n\nfiltered = df[(df[\"date\"] >= start) & (df[\"date\"] <= end)]\nst.dataframe(filtered)",
        "usecase": "Time-range filters over datasets and reports — revenue windows, audit trails, campaign periods — with real date typing end to end.",
        "category": "streamlit"
    },
    {
        "id": 24,
        "title": "st.file_uploader ingests user files",
        "definition": "st.file_uploader accepts file uploads of specified type — csv, xlsx, images — returning an UploadedFile that acts like a file object and stays in memory for the session. Read it with pandas.read_csv(uploaded) or bytes(uploaded.getvalue()); multiple=True allows several files at once.",
        "example": "import streamlit as st\nimport pandas as pd\n\nup = st.file_uploader(\"Upload CSV\", type=[\"csv\"])\nif up is not None:\n    df = pd.read_csv(up)\n    st.dataframe(df.head())\n    st.write(f\"{len(df)} rows\")",
        "usecase": "Self-service data tools where users bring their own spreadsheets or images and the app analyzes them instantly without a storage pipeline.",
        "category": "streamlit"
    },
    {
        "id": 25,
        "title": "st.download_button exports files",
        "definition": "st.download_button turns any bytes or string into a downloadable file with a chosen name and MIME type — the counterpart of file_uploader for exporting. Generate the content on the fly (CSV from a DataFrame, PNG from a chart) and the browser saves it directly.",
        "example": "import streamlit as st\nimport pandas as pd\n\ndf = pd.DataFrame({\"a\": [1, 2], \"b\": [3, 4]})\ncsv = df.to_csv(index=False)\n\nst.download_button(\"Download CSV\", csv, file_name=\"export.csv\", mime=\"text/csv\")",
        "usecase": "Export buttons on every dashboard — filtered tables as CSV, reports as markdown, images as PNG — so users leave with the data they see.",
        "category": "streamlit"
    },
    {
        "id": 26,
        "title": "st.dataframe is interactive and fast",
        "definition": "st.dataframe renders a pandas, polars or arrow DataFrame as an interactive grid with sorting, column resizing and search — backed by a virtualized renderer that handles hundreds of thousands of rows. Unlike st.table it's the modern, feature-rich default for displaying tabular data.",
        "example": "import streamlit as st\nimport pandas as pd\n\ndf = pd.read_csv(\"sales.csv\")   # even 500k rows is fine\nst.dataframe(df, use_container_width=True)\nst.dataframe(df, column_config={\"revenue\": st.column_config.NumberColumn(format=\"$%.2f\")})",
        "usecase": "Displaying large result sets with built-in sorting and searching — the workhorse table widget for data-heavy internal tools.",
        "category": "streamlit"
    },
    {
        "id": 27,
        "title": "st.table is static and lightweight",
        "definition": "st.table renders a simple, non-interactive table — no sorting, no search, no virtualization — which makes it the right choice for small, stable datasets where interactions would be noise: config summaries, small lookups, fixed reference data.",
        "example": "import streamlit as st\nimport pandas as pd\n\nconfig = pd.DataFrame({\"key\": [\"db\", \"port\"], \"value\": [\"postgres\", \"5432\"]})\nst.table(config)   # plain, static, always identical",
        "usecase": "Reference tables and fixed summaries where interactivity adds nothing — keep the heavy sorting machinery for dataframes that need it.",
        "category": "streamlit"
    },
    {
        "id": 28,
        "title": "st.line_chart plots time series instantly",
        "definition": "st.line_chart takes a dataframe, series or array and renders a line chart in one call — no plotting library setup. Column names become series, the index becomes the x-axis. st.area_chart and st.bar_chart are the siblings for stacked area and bar views; all three accept x= and y= to control the mapping.",
        "example": "import streamlit as st\nimport pandas as pd\n\nidx = pd.date_range(\"2026-01-01\", periods=30)\ndf = pd.DataFrame({\"rev\": range(30), \"cost\": [x * 0.6 for x in range(30)]}, index=idx)\n\nst.line_chart(df)              # one line per column\nst.bar_chart(df[\"rev\"])",
        "usecase": "Trends, time series and comparisons from a DataFrame in one line — the default chart for most dashboard quick-wins.",
        "category": "streamlit"
    },
    {
        "id": 29,
        "title": "st.map plots lat/lng points",
        "definition": "st.map renders a scatter overlay on a map (Deck.GL under the hood) from a dataframe with latitude and longitude columns — color, size and hover via color=, size=, hover_data=. For richer maps (layers, tiles, GeoJSON) there's st.pydeck_chart; for most point-overlay needs st.map is enough.",
        "example": "import streamlit as st\nimport pandas as pd\n\npoi = pd.DataFrame({\n    \"lat\": [40.71, 34.05, 51.50],\n    \"lon\": [-74.00, -118.24, -0.12],\n    \"size\": [50, 30, 70],\n})\nst.map(poi, size=\"size\", color=\"#ff0000\")",
        "usecase": "Plotting store locations, delivery points, sensor sites or user geography in one call, with sizing by a metric like volume.",
        "category": "streamlit"
    },
    {
        "id": 30,
        "title": "st.plotly_chart embeds Plotly graphs",
        "definition": "st.plotly_chart renders a Plotly figure with full interactivity — zoom, hover tooltips, legend toggling — the standard for charts users want to explore. Pass use_container_width=True to fill the column; for Altair and Bokeh, st.altair_chart and st.bokeh_chart are the equivalents.",
        "example": "import streamlit as st\nimport plotly.express as px\n\ndf = px.data.gapminder()\nfig = px.scatter(df, x=\"gdpPercap\", y=\"lifeExp\", size=\"pop\", color=\"continent\", log_x=True)\nst.plotly_chart(fig, use_container_width=True)",
        "usecase": "Exploratory dashboards where users zoom into regions, hover for exact values and toggle series — interactivity without custom JS.",
        "category": "streamlit"
    },
    {
        "id": 31,
        "title": "st.pyplot captures matplotlib figures",
        "definition": "st.pyplot renders a matplotlib Figure (or the current pyplot state) into the app — the bridge for all existing matplotlib code. Call st.pyplot(fig) with an explicit figure to avoid state bleed, and call plt.close(fig) afterwards to prevent memory growth in long-running sessions.",
        "example": "import streamlit as st\nimport matplotlib.pyplot as plt\n\nfig, ax = plt.subplots()\nax.plot([1, 3, 2, 4], marker=\"o\")\nax.set_title(\"Trend\")\nst.pyplot(fig)\nplt.close(fig)",
        "usecase": "Reusing established matplotlib analysis code — scientific plots, custom axes, subplot grids — directly inside a Streamlit app.",
        "category": "streamlit"
    },
    {
        "id": 32,
        "title": "st.metric shows a KPI with delta",
        "definition": "st.metric renders a headline number with an optional delta — a colored up/down arrow and percentage vs the previous period. Deltas with delta_color=\"inverse\" flip semantics when down is good (churn, latency). It's the canonical widget for the top row of any dashboard.",
        "example": "import streamlit as st\n\nst.metric(\"Revenue\", \"$1.2M\", delta=\"8.3%\", delta_color=\"normal\")\nst.metric(\"Churn\", \"3.1%\", delta=\"-0.4%\", delta_color=\"inverse\")\nst.metric(\"Active users\", 4240, delta=230)",
        "usecase": "Executive KPI rows where each metric is a number, a comparison to last period, and an immediate good/bad signal.",
        "category": "streamlit"
    },
    {
        "id": 33,
        "title": "st.progress and st.status track long work",
        "definition": "st.progress renders a progress bar with an optional text label; st.status wraps a whole workflow in a collapsible status card with states like 'running' then .update(label=..., state=\"complete\"). Both give long-running steps a visible, living UI instead of a frozen screen.",
        "example": "import streamlit as st\nimport time\n\nwith st.status(\"Processing data...\") as status:\n    for i in range(5):\n        st.write(f\"Step {i + 1}...\")\n        time.sleep(0.2)\n        st.progress((i + 1) / 5)\n    status.update(label=\"Processing complete\", state=\"complete\", expanded=False)",
        "usecase": "ETL jobs, model training and batch operations where the user should see step-by-step progress and a clear completion state.",
        "category": "streamlit"
    },
    {
        "id": 34,
        "title": "st.spinner wraps quick waits",
        "definition": "st.spinner shows a transient 'running' indicator while its context block executes — the lightweight cousin of progress bars for operations that take seconds rather than minutes. Content inside the with block isn't shown; the spinner is replaced by whatever follows once the block finishes.",
        "example": "import streamlit as st\nimport time\n\nwith st.spinner(\"Fetching data...\"):\n    time.sleep(1.5)\n    data = fetch_data()\n\nst.line_chart(data)",
        "usecase": "Every loading phase in a dashboard — API calls, file parsing, dataframe joins — signals clearly that the app is working, not frozen.",
        "category": "streamlit"
    },
    {
        "id": 35,
        "title": "st.success, st.info, st.warning, st.error",
        "definition": "The four alert boxes render color-coded feedback messages: st.success for positive results, st.info for hints, st.warning for caution, st.error for failures. They're for transient, human-readable status — contrast with st.metric and charts which carry the data itself.",
        "example": "import streamlit as st\n\nst.success(\"Export complete — 42 rows written.\")\nst.info(\"Data refreshes hourly at :00.\")\nst.warning(\"Some rows were skipped (3 invalid dates).\")\nst.error(\"Connection to the database failed.\")",
        "usecase": "Instant feedback on every user action — form results, save confirmations, partial failures — using color to communicate severity at a glance.",
        "category": "streamlit"
    },
    {
        "id": 36,
        "title": "st.toast fires non-blocking notifications",
        "definition": "st.toast displays a brief notification in the corner without interrupting the page — the lightweight alternative to st.snackbar (which can be positioned) for one-off confirmations like 'Saved' or 'Copied'. Toast calls vanish after a few seconds, so use them for acknowledgements, not critical errors.",
        "example": "import streamlit as st\n\nif st.button(\"Save\"):\n    save_settings()\n    st.toast(\"Settings saved\", icon=\"✅\")\n\nif st.button(\"Copy link\"):\n    st.toast(\"Link copied to clipboard\")",
        "usecase": "Non-interrupting confirmations for quick actions — saves, copies, small exports — where a full alert box would be overkill.",
        "category": "streamlit"
    },
    {
        "id": 37,
        "title": "st.balloons and st.snow celebrate events",
        "definition": "st.balloons() and st.snow() launch playful full-screen animations — the framework's built-in confetti for successful milestones. Fun and memoable, they're best used sparingly: after a completed training run, a record-breaking metric, or a first successful deploy.",
        "example": "import streamlit as st\n\nif st.button(\"Train model\"):\n    acc = train()\n    st.metric(\"Accuracy\", f\"{acc:.2%}\")\n    if acc > 0.95:\n        st.balloons()\n    else:\n        st.snow()",
        "usecase": "Celebrating thresholds in demos and internal tools — a visible 'you did it' moment that makes milestones feel real.",
        "category": "streamlit"
    },
    {
        "id": 38,
        "title": "st.form batches widgets into one submit",
        "definition": "st.form groups widgets so their values are only read after one Submit button — the script reruns once with all values, not on every change. Any widget inside the form is inert until submission, which is exactly the semantics of a traditional form and avoids premature reruns and flicker.",
        "example": "import streamlit as st\n\nwith st.form(\"signup\"):\n    name = st.text_input(\"Name\")\n    age = st.number_input(\"Age\", 0, 120)\n    submitted = st.form_submit_button(\"Create profile\")\n\nif submitted:\n    st.session_state.profile = {\"name\": name, \"age\": age}\n    st.success(\"Profile created\")",
        "usecase": "Input forms where changing one field must not trigger analysis — profile creation, query builders, settings panels — until the user commits.",
        "category": "streamlit"
    },
    {
        "id": 39,
        "title": "st.chat_input and st.chat_message build chat UIs",
        "definition": "st.chat_input provides a text box whose return is the user's message; st.chat_message(\"user\") / (\"assistant\") render aligned message bubbles. Loop through a message list — storing it in session_state — and append each new exchange to get a full chat interface in pure Python.",
        "example": "import streamlit as st\n\nif \"msgs\" not in st.session_state:\n    st.session_state.msgs = []\n\nfor m in st.session_state.msgs:\n    with st.chat_message(m[\"role\"]):\n        st.write(m[\"content\"])\n\nprompt = st.chat_input(\"Ask me anything\")\nif prompt:\n    st.session_state.msgs.append({\"role\": \"user\", \"content\": prompt})\n    reply = my_llm(prompt)   # any model call\n    st.session_state.msgs.append({\"role\": \"assistant\", \"content\": reply})\n    st.rerun()",
        "usecase": "LLM assistants, support bots and data-Q&A tools built on any backend — the canonical pattern for chat apps in Streamlit.",
        "category": "streamlit"
    },
    {
        "id": 40,
        "title": "@st.cache_data memoizes expensive calls",
        "definition": "Decorating a function with @st.cache_data makes its results cached by inputs: reruns that call it with the same arguments hit the cache instead of re-running the work. The cache respects the function's hashable args, has a configurable TTL, and is the single biggest performance lever for data loading and heavy computation in Streamlit apps.",
        "example": "import streamlit as st\nimport pandas as pd\n\n@st.cache_data(ttl=3600)\ndef load_sales():\n    return pd.read_csv(\"sales.csv\")   # runs once per hour, not per click\n\n@st.cache_data\ndef expensive(df, window=30):\n    return df.rolling(window).mean()\n\nst.line_chart(expensive(load_sales()))",
        "usecase": "Every dashboard that reads a file, queries a database or transforms a dataset — caching converts per-click recomputation into per-argument memoization.",
        "category": "streamlit"
    },
    {
        "id": 41,
        "title": "@st.cache_resource for non-serializable objects",
        "definition": "@st.cache_resource caches objects that can't be pickled for @st.cache_data: database connections, HTTP clients, ML models, thread pools. It holds ONE instance per function shared across the session — perfect for a shared sqlite connection or a loaded model that should be created once.",
        "example": "import streamlit as st\nimport sqlite3\n\n@st.cache_resource\ndef get_db():\n    conn = sqlite3.connect(\"app.db\", check_same_thread=False)\n    return conn\n\n@st.cache_resource\ndef get_model():\n    from transformers import pipeline\n    return pipeline(\"sentiment-analysis\")   # downloads/loads once\n\nconn = get_db()\nmodel = get_model()",
        "usecase": "Expensive one-time setup — model weights, database pools, heavy clients — created exactly once per session and reused by every rerun.",
        "category": "streamlit"
    },
    {
        "id": 42,
        "title": "st.rerun re-executes the script",
        "definition": "st.rerun() aborts the current run and immediately reruns the script from the top — the escape hatch for flows that need a fresh pass: after saving to session_state, switching tabs, or clearing a cache. It's the explicit way to move the app to a new state, cleaner than relying on implicit widget-driven reruns.",
        "example": "import streamlit as st\n\nif \"step\" not in st.session_state:\n    st.session_state.step = 1\n\nif st.button(\"Next\"):\n    st.session_state.step += 1\n    st.rerun()   # fresh rerun with updated state\n\nst.write(f\"Step {st.session_state.step}\")",
        "usecase": "Multi-step wizards, reset buttons and state-driven navigation where the UI must immediately reflect a changed session_state.",
        "category": "streamlit"
    },
    {
        "id": 43,
        "title": "st.stop halts the script early",
        "definition": "st.stop() halts execution of the script at that point without crashing — elements below never render, and Streamlit shows an info 'stopped' indicator. It's the clean way to gate content: if a filter is empty or data is missing, stop before drawing charts that would mislead.",
        "example": "import streamlit as st\nimport pandas as pd\n\nup = st.file_uploader(\"Upload CSV\")\nif up is None:\n    st.info(\"Upload a file to continue\")\n    st.stop()\n\ndf = pd.read_csv(up)\nif df.empty:\n    st.warning(\"File has no rows\")\n    st.stop()\n\nst.dataframe(df)\nst.line_chart(df)", 
        "usecase": "Guard rails in data apps: stop the script when prerequisites are missing so downstream sections never render incomplete or misleading output.",
        "category": "streamlit"
    },
    {
        "id": 44,
        "title": "st.set_page_config controls the page shell",
        "definition": "st.set_page_config sets the page title (browser tab), icon, layout (\"centered\" or \"wide\"), sidebar state and initial sidebar collapsed state. It must be the first Streamlit command in the script. Wide layout plus expanded sidebar is the standard dashboard configuration.",
        "example": "import streamlit as st\n\nst.set_page_config(\n    page_title=\"Sales Dashboard\",\n    page_icon=\"📈\",\n    layout=\"wide\",\n    initial_sidebar_state=\"expanded\",\n)\n\nst.title(\"Sales Dashboard\")",
        "usecase": "Branding every app — title, favicon, wide layout for dashboards with many columns — from the very first line of the script.",
        "category": "streamlit"
    },
    {
        "id": 45,
        "title": "st.secrets keeps credentials out of code",
        "definition": "st.secrets reads from .streamlit/secrets.toml and its environment overrides: st.secrets[\"api_key\"]. Values are accessible only server-side and never sent to the browser. It's the sanctioned way to store API keys and database credentials in Streamlit Cloud and local dev alike — never hardcode secrets into the script.",
        "example": "# .streamlit/secrets.toml\n# [db]\n# url = \"postgresql://user:pass@host/db\"\n\nimport streamlit as st\n\nconn = st.connection(\"db\")   # reads st.secrets[\"db\"]\nkey = st.secrets[\"api_key\"]\nst.write(\"Connected\" if conn else \"no\")",
        "usecase": "Deploying apps with API keys, DB URLs and third-party tokens that exist in secrets files and env vars, never in source control.",
        "category": "streamlit"
    },
    {
        "id": 46,
        "title": "st.connection is the data-access shortcut",
        "definition": "st.connection creates typed connections from st.secrets: st.connection(\"db\") returns a SQLAlchemy-backed connection usable as a context manager (conn.query(\"SELECT ...\")) and st.connection(\"s3\", type=\"filesystem\") handles object stores. It configures from secrets, caches the connection with cache_resource semantics, and removes hand-rolled connection boilerplate.",
        "example": "import streamlit as st\n\nconn = st.connection(\"db\")       # configured via .streamlit/secrets.toml\nrows = conn.query(\"SELECT region, SUM(revenue) FROM sales GROUP BY 1\", ttl=600)\nst.dataframe(rows)\n\nfs = st.connection(\"s3\", type=\"filesystem\")\nfor f in fs.fs.glob(\"daily/*.csv\"):\n    print(f)",
        "usecase": "Dashboards that query Postgres/MySQL/Snowflake and read cloud storage with a few lines — configuration, caching and cleanup handled for you.",
        "category": "streamlit"
    },
    {
        "id": 47,
        "title": "st.fragment scopes reruns to a section",
        "definition": "Decorating a function with @st.fragment wraps its widgets so interactions rerun only that fragment, not the whole script — big performance win for apps with expensive global loading plus an interactive widget. Fragments also support st.rerun(scope=\"fragment\") to refresh just their own section.",
        "example": "import streamlit as st\n\n@st.cache_data\ndef load_big():\n    return get_full_dataset()   # expensive, global\n\n@st.fragment\ndef filter_panel():\n    metric = st.selectbox(\"Metric\", [\"rev\", \"cost\"])\n    st.line_chart(load_big()[metric])   # only this reruns on change\n\nst.header(\"Dashboard\")\nfilter_panel()\nst.write(\"Global footer — not rerun on metric change\")",
        "usecase": "Interactive widgets on top of expensive global state — only the chart section reruns, the full-page recompute happens once.",
        "category": "streamlit"
    },
    {
        "id": 48,
        "title": "st.audio and st.video play media",
        "definition": "st.audio renders an audio player for files, bytes or URLs (format=\"audio/wav\" etc.), and st.video does the same for video files with start_time and end_time controls. Loop, autoplay and format are configurable — the quick path to embedding recordings, demos and clips in a data app.",
        "example": "import streamlit as st\n\nst.audio(\"podcast.mp3\", format=\"audio/mpeg\", autoplay=False)\nst.video(\"demo.mp4\", start_time=10, end_time=20)\n\nwith open(\"recording.wav\", \"rb\") as f:\n    st.audio(f.read(), format=\"audio/wav\")",
        "usecase": "Analysis tools that play back recordings or clips alongside the data — QA dashboards, model-evaluation reviews, meeting transcription viewers.",
        "category": "streamlit"
    },
    {
        "id": 49,
        "title": "st.image displays images and captions",
        "definition": "st.image accepts a file path, URL, numpy array or PIL image, with width, caption and use_container_width options. Arrays render directly, so computer-vision apps can show inference results without saving files. For PIL objects pass the image itself; for arrays with a batch dimension, give a list.",
        "example": "import streamlit as st\nfrom PIL import Image\n\nimg = Image.open(\"photo.jpg\")\nst.image(img, caption=\"Original\", width=400)\n\nst.image(\"https://picsum.photos/400\", caption=\"Remote image\")\nst.image(np_array, caption=\"Camera frame\")",
        "usecase": "Photo galleries, CV demos showing model output overlaid on frames, and documentation-style apps embedding diagrams inline.",
        "category": "streamlit"
    },
    {
        "id": 50,
        "title": "Run a Streamlit app with streamlit run",
        "definition": "python -m streamlit run app.py (or streamlit run app.py) starts the local server, opening the app in a browser tab at localhost:8501 with hot-reload on save. Streamlit Cloud deploys a repo by running the same command, so local and production runs are identical — the simplest path from script to shared URL.",
        "example": "# terminal\nstreamlit run app.py\n# -> Local URL: http://localhost:8501\n\n# watch mode (hot reload)\nstreamlit run app.py --server.headless false\n\n# deploy\n# push to GitHub, then Streamlit Community Cloud runs streamlit run app.py",
        "usecase": "Every Streamlit workflow starts here — local iteration with hot reload, then deploying the same command to Cloud for shared access.",
        "category": "streamlit"
    },
]
