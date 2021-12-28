import numpy as np
import pandas as pd
import plotly.express as px

def update_order_book(bid_price, quantity, book_df, const_fee, partial=False):
    """Finds and fills the booked order based on the order bid price and desired asset quantity, if it is not possible returns
    the original book order data frame. To sell asset at the specified price negative quantity has to be provided.
    If the input for partial=True then if there is not enough supply at the market for the right price, only part of the
    order will be filled; if partial=False, then in case of not enough supply the order will not be filled at all. In case of
    successful transaction the order book is updated"""
    
    if (const_fee<0) or (const_fee>0.03):
        raise ValueError("const_fee must take value in [0.0, 0.03]")
    
    #Order book prices and bid price both have to have 2 decimal points
    book_df = book_df.round(decimals=2)
    bid_price = np.round(bid_price, decimals=2)
    
    #Match the price of the bid with the price in the order book
    matching_price_series=book_df[book_df["Price"]==bid_price]["Quantity"]
    
    
    if quantity > 0:
        matching_price_series=matching_price_series[matching_price_series>=0]
        quantity_check=(matching_price_series-quantity)
        
        #Looking for the closest quantity on the market above the provided quantity
        higher_quantity = quantity_check[quantity_check>=0]
        if len(higher_quantity)>0:
            best_offers = higher_quantity[higher_quantity==higher_quantity.sort_values().iloc[0]]
            filled_market_order=best_offers.index[0]
            print("The market order getting filled:\n", book_df.iloc[filled_market_order])
            book_df["Quantity"].iloc[filled_market_order] = book_df["Quantity"].iloc[filled_market_order]-quantity
            print("Your order has been completely filled")
            print("Total number of transactions: 1")
            print("Total fees accumulated:", quantity*(book_df["Price"].iloc[filled_market_order])*const_fee)
            #Update the order book
            if (book_df["Quantity"].iloc[filled_market_order])>0:
                return book_df
            else:
                return book_df.drop(filled_market_order, axis=0)
        
        elif len(higher_quantity)==0 and partial==False:
            print("No order on the market satisfies the criteria, try partially filling it")
            return book_df
        
        elif len(higher_quantity)==0 and partial==True:
            all_offers=quantity_check.sort_values(ascending=False)
            quantity_to_fill = quantity
            filled_market_orders=[]
            filled_quantity=0
            number_of_transactions=0
            fees_accumulated=0
            while (quantity_to_fill > 0) and (len(all_offers)!=0):
                print("The market order getting filled:\n", book_df.iloc[all_offers.index[0]])
                quantity_to_fill = quantity_to_fill-book_df["Quantity"].iloc[all_offers.index[0]]
                if quantity_to_fill < 0:
                    filled_quantity = filled_quantity+book_df["Quantity"].iloc[all_offers.index[0]]+quantity_to_fill
                    fees_accumulated = fees_accumulated+(book_df["Quantity"].iloc[all_offers.index[0]]
                                                         +quantity_to_fill)*bid_price*const_fee
                    book_df["Quantity"].iloc[all_offers.index[0]] = -quantity_to_fill
                    quantity_to_fill = 0
                else:
                    filled_quantity = filled_quantity+book_df["Quantity"].iloc[all_offers.index[0]]
                    fees_accumulated = fees_accumulated+book_df["Quantity"].iloc[all_offers.index[0]]*bid_price*const_fee
                    book_df["Quantity"].iloc[all_offers.index[0]] = 0
                    filled_market_orders.append(all_offers.index[0])
                all_offers.drop(all_offers.index[0], axis=0, inplace=True)
                number_of_transactions = number_of_transactions+1
            if filled_quantity==quantity:
                print("Your order has been completely filled")
            else:
                print(filled_quantity, "of your order has been filled.")
            print("Total number of transactions:", number_of_transactions)
            print("Total fees accumulated:", fees_accumulated)
            return book_df.drop(filled_market_orders, axis=0)
        
        else:
            return book_df
      
    
    elif quantity < 0:
        matching_price_series=matching_price_series[matching_price_series<=0]
        quantity_check=(matching_price_series-quantity)
        
        #Looking for the closest quantity on the market above the provided quantity
        higher_quantity=quantity_check[quantity_check<=0]
        if len(higher_quantity)>0:
            best_offers=higher_quantity[higher_quantity==higher_quantity.sort_values().iloc[-1]]
            filled_market_order=best_offers.index[0]
            print("The market order getting filled:\n", book_df.iloc[filled_market_order])
            book_df["Quantity"].iloc[filled_market_order] = book_df["Quantity"].iloc[filled_market_order]-quantity
            print("Your order has been completely filled")
            print("Total number of transactions: 1")
            print("Total fees accumulated:", -quantity*(book_df["Price"].iloc[filled_market_order])*const_fee)
            #Update the order book
            if (book_df["Quantity"].iloc[filled_market_order])<0:
                return book_df
            else:
                return book_df.drop(filled_market_order, axis=0)
        
        elif len(higher_quantity)==0 and partial==False:
            print("No order on the market satisfies the criteria, try partially filling it")
            return book_df
        
        elif len(higher_quantity)==0 and partial==True:
            all_offers=quantity_check.sort_values(ascending=True)
            quantity_to_fill = quantity
            filled_market_orders=[]
            filled_quantity=0
            number_of_transactions=0
            fees_accumulated=0
            while (quantity_to_fill < 0) and (len(all_offers)!=0):
                print("The market order getting filled:\n", book_df.iloc[all_offers.index[0]])
                quantity_to_fill = quantity_to_fill-book_df["Quantity"].iloc[all_offers.index[0]]
                if quantity_to_fill > 0:
                    filled_quantity = filled_quantity+book_df["Quantity"].iloc[all_offers.index[0]]+quantity_to_fill
                    fees_accumulated = fees_accumulated-(book_df["Quantity"].iloc[all_offers.index[0]]+quantity_to_fill)*bid_price*const_fee
                    book_df["Quantity"].iloc[all_offers.index[0]] = -quantity_to_fill
                    quantity_to_fill = 0
                else:
                    filled_quantity = filled_quantity+book_df["Quantity"].iloc[all_offers.index[0]]
                    fees_accumulated = fees_accumulated-book_df["Quantity"].iloc[all_offers.index[0]]*bid_price*const_fee
                    book_df["Quantity"].iloc[all_offers.index[0]] = 0
                    filled_market_orders.append(all_offers.index[0])
                all_offers.drop(all_offers.index[0], axis=0, inplace=True)
                number_of_transactions = number_of_transactions+1
            if filled_quantity==quantity:
                print("Your order has been completely filled")
            else:
                print(filled_quantity, "of your order has been filled.")
            print("Total number of transactions:", number_of_transactions)
            print("Total fees accumulated:", fees_accumulated)
            return book_df.drop(filled_market_orders, axis=0)
    
    else:
        return book_df


if __name__ == "__main__":

    #Simple order book example
    #Positive values in this dataframe mean "ready to sell, negative are "ready to buy"
    modf=pd.DataFrame(np.array([[10.0, 10.01, 10.0, 10.02, 10.0], [5, 12, 7, 6, 9]]).transpose(), columns=["Price", "Quantity"])
    
    print(update_order_book(10.0, 15,  modf, 0.01, partial=True))