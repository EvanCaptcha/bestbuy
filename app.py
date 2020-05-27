import requests
from discord_webhook import DiscordEmbed, DiscordWebhook

webhookurl = 'https://discord.com/api/webhooks/712487108299718666/g1z8UsfR6K-bqGPtrOtVDnD0FBoV51o7nksgJ70JimL1knSICrpGWBbKlJXwIxkkKfag'
def sendHook(content):
    webhook = DiscordWebhook(url=webhookurl)
    embed = DiscordEmbed(title='Target Instore Monitor',description= content + '\nBestBuy Instore by jxn',color=int('009000'))
    webhook.add_embed(embed)
    webhook.execute()
class product:
    def __init__(self, product):
        self.product = product
        self.avail = False
    def inStock(self):
        self.avail = True
    def OutOfStock(self):
        self.avail = False

headers = {
    'authority': 'www.bestbuy.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'origin': 'https://www.bestbuy.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'content-type': 'application/json',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://www.bestbuy.com/site/nintendo-switch-32gb-lite-gray/6257135.p?skuId=6257135',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9'}

def monitor(zip, sku):
    data = '{"locationId":455,"zipCode":"' + zip + '","showOnShelf":true,"lookupInStoreQuantity":false,"xboxAllAccess":false,"consolidated":false,"showOnlyOnShelf":false,"showInStore":false,"pickupTypes":null,"items":[{"sku":"'+ sku + '","condition":null,"quantity":1,"itemSeqNumber":"1","reservationToken":null,"selectedServices":[],"requiredAccessories":[],"isTradeIn":false}]}'
    response = requests.post('https://www.bestbuy.com/productfulfillment/c/api/2.0/storeAvailability', headers=headers, data=data).json()
    print(response['ispu']['items'][0])
    isAvail = response['ispu']['items'][0]['ispuEligible']
    while not isAvail:
        response = requests.post('https://www.bestbuy.com/productfulfillment/c/api/2.0/storeAvailability',headers=headers, data=data).json()
        status = response['ispu']['items'][0]['pickupEligible']
        if status:
            print("Status: InStock")
            isAvail = True
        else:
            print("Status: OOS")


    while isAvail:
        response = requests.post('https://www.bestbuy.com/productfulfillment/c/api/2.0/storeAvailability',headers=headers, data=data).json()
        for location in response['ispu']['items'][0]['locations']:
            if 'availability' in location:
                locId = location['locationId']
                locId = product(f"{sku}")
                if not locId.avail:
                    print(location)
                    sendHook(f'{location["locationId"]} loaded stock on product {sku}')
                    locId.inStock()
                else:
                    pass






monitor(zip='10514', sku='6350870')
