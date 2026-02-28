.PHONY: download_data transform_data run_dashboard remove_data all

all: download_data transform_data run_dashboard

download_data: download_data.py
	python download_data.py

transform_data: transfrom.py data/apple_sales_data.csv
	python transfrom.py

run_dashboard: app.py data/apple_sales_data_transformed.csv
	streamlit run app.py

remove_data:
	python -c "import os; os.remove('data/apple_sales_data.csv') if os.path.exists('data/apple_sales_data.csv') else None"