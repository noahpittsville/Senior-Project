# METHOD 1
def getClient():
    client = tweepy.Client(bearer_token = config.BEARER_TOKEN,
                           consumer_key = config.API_KEY,
                           consumer_secret = config.API_KEY_SECRET,
                           access_token=config.ACCESS_TOKEN,
                           access_token_secret = config.ACCESS_TOKEN_SECRET)
    return client

def getUserName():
    client = getClient()
    user = client.get_user(username='Tesla')
    return user.data
def getUserID():
    client = getClient()
    user = client.get_user(username='Tesla')
    return user.data.id

# TEST
#username = getUserName()
#userid = getUserID()
#print(username, userid)









class GrabLimit():
    def __init__(self, grab_limit=300):
        self._grab_limit = grab_limit
    def get_grab_limit(self):
        return self._grab_limit
    def set_grab_limit(self, grab):
        self._grab_limit = grab

class Array(object):
    def __init__(self, size, defaultValue = None):
        self.size = size
        if(defaultValue == None):
            self.items = list()
            for i in range(size):
                self.items.append(defaultValue)
        else:
            self.items = list()
            if(len(defaultValue) == size or len(defaultValue) < size):
                for j in range(len(defaultValue)):
                    if(defaultValue[j]):
                        self.items.append(defaultValue[j])
                for i in range(len(defaultValue), size):
                    self.items.append(None)
            else:
                print('Too many elements for the specified size')
    def Length(self):
        length = 0
        for i in self.items:
            if i == None:
                continue
            else:
                length += 1
        return length
    def Search(self, element):
        if element in self.items:
            position = 0
            for i in range(self.Length()):
                if(self.items[i] == element):
                    break
                else:
                    position += 1

            print('{} found at position {}.'.format(element, position))
            return True
        else:
            print('{} not found.'.format(element))
            return False
    def Delete(self, element):
        if element in self.items:
            Index = self.items.index(element)
            self.items[Index] = None
            self.items = list(filter(None, self.items))
        else:
            print('{} not found.'.format(element))
    def Add(self, element):
        if element in self.items:
            print('{} already added to the list. ')
        else:
            self.items.append(element)