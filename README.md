Kenyan NSE Dashboard
Steps Followed to Build the Dashboard

    Data Loading

        Read CSV file using pandas, handling comma-separated thousands in the Volume column.

        Parsed dates with %d-%b-%y format.

        Removed index rows (codes starting with ^) to keep only stock data.

        Converted numeric columns (prices, change, volume) to proper numeric types.

    Data Cleaning

        Replaced missing or placeholder - values with 0 in Change%.

        Filled Volume NaNs with 0 and converted to integer.

        Ensured all price columns are numeric for calculations.

    Interactive Filters

        Date range slider – selects a period of interest.

        Stock code multiselect – allows viewing one or multiple stocks.

        Name search – filters by company name substring.

    Key Performance Indicators (KPIs)

        Total Volume (shares)

        Average Day Price

        Maximum Day High

        Number of unique stocks in filtered data

        Estimated Turnover (Day Price × Volume)

        Average percentage change

        Earliest and latest dates in the filtered view

    Visualizations

        Line chart – shows Day Price evolution over time, colored by stock code.

        Bar chart – total volume per stock.

        Heatmap – average price per stock for each weekday (reveals weekly patterns).

        Top gainers/losers table based on the latest date’s Change%.

    Data Table & Export

        Displays the filtered dataset in an interactive table.

        Provides a CSV download button for filtered results.

    Deployment

        Built with Streamlit (Python) for rapid interactive web apps.

        Deployed to Streamlit Cloud by pushing the code and data file to a GitHub repository, then connecting the repo to Streamlit.

        No external database required; the CSV file is embedded.
