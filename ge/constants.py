with open('../data/item_ids.txt') as fp:
    ALL_ITEMS = [int(item) for item in fp.read().split(',')]

HEADERS = {
    'User-Agent': 'Daily Querying Through all Items for Data Science - Thanks for the cool data!',
    'From': 'https://github.com/CameronChandler/grandexchange'
}