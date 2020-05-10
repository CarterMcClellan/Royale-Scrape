from bs4 import BeautifulSoup
import requests
from pandas import ExcelWriter, DataFrame

CARTER_KEY = "PVQ90YCV"
CHRIS_KEY = "2JV9RJYJG"
DAD_KEY = "L8RCCJGV"

# Return parsed profile page using BS4
def parseURL(tag, sort_by):
    if sort_by == "level":
         link = "https://statsroyale.com/profile/{}/cards?sort=level".format(tag)
    elif sort_by == "elixir":
        link = "https://statsroyale.com/profile/{}/cards?sort=exlixir".format(tag)
    elif sort_by == "rarity":
        link = "https://statsroyale.com/profile/{}/cards?sort=rarity".format(tag)
    elif sort_by == "arena":
        link = "https://statsroyale.com/profile/{}/cards?sort=arena".format(tag)
    
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'html.parser')
    return soup



class Card:
    def __init__(self, card_html):
        self.name, self.level, self.curr_count, self.rarity = self.parse(card_html)
    
    def parse(self, card_html):
        rarity_map = {
            "1" : "Common", 
            "2" : "Rare",
            "3" : "Epic",
            "4" : "Legendary"
        }
        name = card_html.find("div", {"class" : "ui__tooltip ui__tooltipTop ui__tooltipMiddle cards__tooltip"}).text.replace('\n','')
        level = card_html.find("a").text.replace('\n','')
        curr_count = card_html.find("div", {"class" : "profileCards__meter__numbers"}).text.replace('\n','')
        rarity = card_html["data-rarity"][0]
        return name, level, curr_count, rarity_map[rarity]
    
    
    def __repr__(self):
        return "{}".format(self.name)
    
    def __hash__(self):
        return hash(self.name)

    def to_row(self):
        return {"Name" : self.name, "Level": self.level, "Count" : self.curr_count, "Rarity" : self.rarity}


def to_df(key, verbose=False):
    carter_soup = parseURL(key, "rarity")
    carter_cards_html = carter_soup.findAll("div", {"class": "profileCards__card upgrade "}) +                         carter_soup.findAll("div", {"class": "profileCards__card "}) +                         carter_soup.findAll("div", {"class": "profileCards__card upgrade"}) +                         carter_soup.findAll("div", {"class": "profileCards__card"})

    carter_card_objs = [Card(card_html) for card_html in carter_cards_html]
    if verbose:
        print("Found {} cards".format(len(carter_card_objs)))
        
    try:
        assert len(carter_card_objs) == len(set(carter_card_objs))
    except AssertionError:
        print("Duplicate Cards Detected and removed")
        carter_card_objs = list(set(carter_card_objs))
    
    if verbose:
        print("After duplicate detection found {} cards".format(len(carter_card_objs)))

    carter_cards = [card_obj.to_row() for card_obj in carter_card_objs]
    df = DataFrame(carter_cards); df.index = df.Name; del df["Name"]
    return df

def save_xls(list_dfs, df_names, xls_path):
    with ExcelWriter(xls_path) as writer:
        for name, df in zip(df_names, list_dfs):
            df.to_excel(writer, name)
        writer.save()

if __name__ == "__main__":
    print("generating carter df")
    carter_df = to_df(CARTER_KEY, verbose=True)

    print("generating chris df")
    chris_df = to_df(CHRIS_KEY, verbose=True)

    print("generating dad df")
    dad_df = to_df(DAD_KEY, verbose=True)

    save_xls([carter_df, chris_df, dad_df], ["carter_df", "chris_df", "dad_df"], "./clash_royale.xlsx")