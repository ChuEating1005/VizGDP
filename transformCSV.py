
import pandas as pd
import json
import csv

# 讀取原始CSV檔案
df = pd.read_csv('public/data/GNH.csv')

# 建立國家與大陸對應的字典

def load_country_codes(json_path):
    # 讀取 JSON 檔案中的國家代碼對應
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def create_mappings(csv_path):
    # 初始化字典
    continent_mapping = {}
    country_code_mapping = {}
    image_url_mapping = {}
    
    # 讀取 ISO 3166-1 代碼對應
    alpha3_to_alpha2 = load_country_codes('public/data/iso3166-1.json')
    
    # 讀取 CSV 檔案
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            country_name = row['Country Name']
            alpha3_code = row['Country Code'].upper()  # 轉換為大寫以匹配 JSON
            alpha2_code = alpha3_to_alpha2.get(alpha3_code, alpha3_code.lower())
            
            # 建立對應關係
            continent_mapping[country_name] = row['Region']
            country_code_mapping[country_name] = alpha3_code
            
            # 更新 Image URL 為 flagcdn.com 格式
            image_url_mapping[country_name] =  f'https://flagcdn.com/w80/{alpha2_code}.png'
    return continent_mapping, country_code_mapping, image_url_mapping

# 使用函數建立對應字典
gdp_data_path = 'public/data/gdpdata.csv'
continent_mapping, country_code_mapping, image_url_mapping = create_mappings(gdp_data_path)

# 重組資料
def transform_data(df):
    # 建立新的資料框架
    years = range(2005, 2024)
    countries = df['Country name'].unique()
    
    # 準備新的資料結構
    new_data = []
    for country in countries:
        
        country_data = {
            'Country Name': country,
            'Continent': continent_mapping.get(country, 'Unknown'),
            'Image URL': image_url_mapping.get(country, 'Unknown'),
            'Country Code': country_code_mapping.get(country, '')
        }
        
        # 加入年度資料
        country_df = df[df['Country name'] == country]
        for year in years:
            year_data = country_df[country_df['year'] == year]
            if not year_data.empty:
                country_data[str(year)] = year_data['Life Ladder'].iloc[0]
            else:
                country_data[str(year)] = None
                
        new_data.append(country_data)
    
    return pd.DataFrame(new_data)

# 轉換資料
new_df = transform_data(df)

# 儲存為新的CSV檔案
new_df.to_csv('transformed_data.csv', index=False)

# 印出前幾筆資料以確認格式
print(new_df.head())