from google.ads.googleads.client import GoogleAdsClient
import csv 
import datetime

today = datetime.datetime.today()

# Формат даты в YYYY-MM-DD
today = today.strftime('%Y-%m-%d')

google_ads_client = GoogleAdsClient.load_from_storage("config/google-ads.yaml")


def return_gclid(ad_group_ad):
    #Запрос для поиска gclid из таблицы click_view
    query = f""" SELECT 
    click_view.gclid
    FROM
    click_view
    WHERE
    segments.date =  '{today}'
    AND
    click_view.keyword = '{ad_group_ad}'
    """
    customer_id = "1958588682"
    google_ads_service = google_ads_client.get_service("GoogleAdsService")
    response = google_ads_service.search(customer_id=customer_id, query=query)
    arr = set()
    #Формирование списка gclid
    for row in response:
        gclid = row.click_view.gclid
        arr.add(gclid)
    if len(arr) != 0:
        arr = list(arr)
        return arr
    else:
        return []



customer_id = "1958588682"

#Формируем запрос
query = f"""SELECT
    search_term_view.ad_group,
    search_term_view.resource_name,
    search_term_view.search_term,
    search_term_view.status,
    segments.date,
    segments.keyword.info.text,
    segments.keyword.ad_group_criterion,
    metrics.impressions,
    metrics.clicks,
    metrics.conversions,
    metrics.cost_micros,
    metrics.cost_per_conversion,
    metrics.cross_device_conversions,
    metrics.conversions_value
    
FROM
    search_term_view
WHERE
    segments.date = '{today}'
    """   

google_ads_service = google_ads_client.get_service("GoogleAdsService")

response = google_ads_service.search(customer_id=customer_id, query=query)



with open("data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(['Customer id', 'Compaint id', 'Ad group id', 'Criterian id', 'Date', 'Status', 'Search term', 'Search term url', 'Clicks', 'Impressions', 'Conversions', 'Cost Micros', 'Cost Per Conversion', 'Conversion Value', 'Cross Device Conversions', 'Keyword Text', 'Gclids'])
    #Обработаем полученные данные
    for row in response:
        rtw = row.search_term_view
        resource = rtw.resource_name.split("/")
        customer_id = resource[1]
        stw = resource[3].split("~")
        copmain_id = stw[0]
        ad_group_id = stw[1]
        search_term_url = stw[2]
        search_term = rtw.search_term
        status = rtw.status
        mtr = row.metrics
        clicks = mtr.clicks
        impressions = mtr.impressions
        conversions = mtr.conversions
        cost_micros = mtr.cost_micros
        cost_per_conversion = mtr.cost_per_conversion
        conversion_value = mtr.conversions_value
        cross_device_conversions = mtr.cross_device_conversions
        sgm = row.segments
        date = sgm.date
        text = sgm.keyword.info.text
        criterian_id = sgm.keyword.ad_group_criterion.split("/")[3].split('~')[1]
        gclids = return_gclid(ad_group_ad=sgm.keyword.ad_group_criterion)

        if len(gclids) == 0:
            gclids = None
        else:
            gclids = ";".join(gclids)

        writer.writerow([customer_id, copmain_id, ad_group_id, criterian_id, date, status, search_term, search_term_url, clicks, impressions, conversions, cost_micros, cost_per_conversion, conversion_value, cross_device_conversions, text, gclids])