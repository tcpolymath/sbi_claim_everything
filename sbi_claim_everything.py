from beem.nodelist import NodeList
from beem import Steem
from beem.instance import set_shared_steem_instance
from beem.account import Account
from steembi.storage import AccountsDB, KeysDB

with open('scot_token_list', 'r') as tokenlist:
	tokens = tokenlist.read().splitlines()
	
config_file = 'config.json'
if not os.path.isfile(config_file):
    raise Exception("config.json is missing")
else:
    with open(config_file) as json_data_file:
        config_data = json.load(json_data_file)
	databaseConnector2 = config_data["databaseConnector2"]

db2=dataset.connect(databaseconnector2)
	
accStorage = AccountsDB(db2)
keyStorage = KeysDB(db2)

accounts = accStorage.get()
	
keys = []
for acc in accounts:
    keys.append(keyStorage.get(acc, "posting"))
keys_list = []
for k in keys:
    if k["key_type"] == 'posting':
        keys_list.append(k["wif"].replace("\n", '').replace('\r', ''))
node_list = nodes.get_nodes(normal=normal, appbase=appbase, wss=wss, https=https)
if "https://api.steemit.com" in node_list:
    node_list.remove("https://api.steemit.com")    
stm = Steem(node=node_list, keys=keys_list, num_retries=5, call_num_retries=3, timeout=15, nobroadcast=nobroadcast)

set_shared_steem_instance(stm)

for account in accounts:
	try:
		Account(account).claim_reward_balance()
		print "Claimed " + account + " rewards."
	except:
		continue
	for scot_token in tokens:
		json_dict = {"symbol":scot_token}
		stm.custom_json('scot_claim_token', json_dict, required_posting_auths=[account])
		print "Claimed " + scot_token + " rewards for " + account

	
