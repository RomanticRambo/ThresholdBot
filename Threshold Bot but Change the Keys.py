import requests
from datetime import datetime
import tweepy

timestamp = int(datetime.now().timestamp())

url = "https://api.etherscan.io/api" + \
   "?module=block" + \
   "&action=getblocknobytime" + \
   f"&timestamp={timestamp}" + \
   "&closest=before" + \
   "&apikey=QBMAG2IV5KQW74M4DFYPHCCICRVZG3GUMW"

block = int(requests.get(url).json()['result'])

sblock = block - 60*60/15

url = "https://api.etherscan.io/api" + \
   "?module=account" + \
   "&action=txlist" + \
   "&address=0x9C070027cdC9dc8F82416B2e5314E11DFb4FE3CD" + \
   f"&startblock={sblock}" + \
   f"&endblock={block}" + \
   "&sort=asc" + \
   "&apikey=QBMAG2IV5KQW74M4DFYPHCCICRVZG3GUMW"

res = requests.get(url)

transactions = res.json()['result']

if not transactions:
   exit()

transactions = [ x for x in transactions if x['methodId'] == '0x6abe3a6c' and int(x['timeStamp']) > timestamp - 30*60 ]
transactions.sort(key=lambda x: int(x['timeStamp']), reverse=True)

url = "https://api.etherscan.io/api" + \
   "?module=logs" + \
   "&action=getLogs" + \
   f"&address={transactions[0]['to']}" + \
   f"&fromBlock={transactions[0]['blockNumber']}" + \
   f"&toBlock={transactions[0]['blockNumber']}" + \
   "&apikey=QBMAG2IV5KQW74M4DFYPHCCICRVZG3GUMW"

logs = requests.get(url).json()['result']

amount = int(logs[0]['data'], 16) / 10**18

address = hex(int(logs[0]['topics'][-1], 16))

timestamp = int(transactions[0]['timeStamp'])



API_KEY = "rBBOC6o550u2IDbmLB6IOqQkf"
API_KEY_SECRET = "TdvPxjiayebOeMGgbfou2h5b83pu6t3Svmze6yw007AKDyVNK6"

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFuargEAAAAAclvMaVqGpsnDqRQRG7cFxImYJcs%3DEEbixNjwqOLnliFUS558ej7mcmNpvflf8l7TGoFxOyt29Jt16L"

ACCESS_TOKEN = "1513567220168855682-Bm9rND1gmW10LFPaRKZtvrZ7IbYWLw"
ACCESS_TOKEN_SECRET = "9xFDF6owvjOto7gbVtTn5SEA6W1B5tDOS4W2yzWIa1wiz"


def get_twitter_conn_v1(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) -> tweepy.API:

   auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET)
   auth.set_access_token(
      ACCESS_TOKEN,
      ACCESS_TOKEN_SECRET,
   )
   return tweepy.API(auth)

client_v1 = get_twitter_conn_v1(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

client = tweepy.Client(
   BEARER_TOKEN, API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

image_path = "attach.png"
media = client_v1.media_upload(image_path)
media_id = media.media_id

tweet = f"NEW tBTC TOKENS MINTED!\n\nAmount: {amount}tBTC\n\nWallet Address: {address}\n\nTime: {datetime.fromtimestamp(timestamp).time()}UTC\n\nTx Hash:etherscan.io/tx/{transactions[0]['hash']}"

client.create_tweet(text=tweet, media_ids=[media_id])
print('tweeted')