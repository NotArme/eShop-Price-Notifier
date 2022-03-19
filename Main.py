from eShopPage import LoadWishlist
from LocalStorage import GetWishlist

def Main():
    wishlist = GetWishlist()

    LoadWishlist(wishlist)



if __name__ == "__main__":
    Main()