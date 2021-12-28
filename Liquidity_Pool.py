import numpy as np
import pandas as pd
import plotly.express as px

def update_liquidity_pool(quantity, liquidity_df , const_fee, token="Token 1"):
    """Finds and fills the  order based on the token and liquidity provided, if it is not possible returns
    the original liquidity data frame. To sell asset at the specified price negative quantity has to be provided. In case of a
    successful transaction the data frame with accumulated fees is returned"""
    
    np.round(liquidity_df, decimals=2)
    
    if (const_fee<0) or (const_fee>0.03):
        raise ValueError("const_fee must take value in [0.0, 0.03]")
    if quantity <=0:
        raise ValueError("quantity has to be a positive value")
    
    if token=="Token 1":
        if quantity > liquidity_df["Token 1 Supply"].iloc[0]:
            print("Not enough token supply to fill your order")
            return liquidity_df
        updated_token_supply = liquidity_df["Token 1 Supply"][0]-quantity
        updated_other_supply = liquidity_df["Char Number"][0]/updated_token_supply
        price_and_fee = updated_other_supply - liquidity_df["Token 2 Supply"][0]
        fee=quantity*const_fee #In terms of Token 1
        price = price_and_fee/(quantity*(1+const_fee))
        print("Your order of ", quantity, " has been filled at the price of", price)
        #Update the liquidity_df
        liquidity_df["Token 1 Supply"][0] = updated_token_supply
        liquidity_df["Token 2 Supply"][0] = updated_other_supply
        liquidity_df["Fees Accumulated"][0] = liquidity_df["Fees Accumulated"][0]+fee #In terms of Token 1
        print("Total number of transactions: 1")
        print("Total fees accumulated:", liquidity_df["Fees Accumulated"][0], "(In terms of Token 1)")
        return liquidity_df 

    elif token=="Token 2":
        if quantity > liquidity_df["Token 2 Supply"].iloc[0]:
            print("Not enough token supply to fill your order")
            return liquidity_df
        updated_token_supply = liquidity_df["Token 2 Supply"][0]-quantity
        updated_other_supply = liquidity_df["Char Number"][0]/updated_token_supply
        price_and_fee = updated_other_supply - liquidity_df["Token 1 Supply"][0]
        fee=quantity*const_fee #In terms of Token 2
        price = price_and_fee/(quantity*(1+const_fee))
        print("Your order of ", quantity, " has been filled at the price of", price)
        #Update the liquidity_df
        liquidity_df["Token 2 Supply"][0] = updated_token_supply
        liquidity_df["Token 1 Supply"][0] = updated_other_supply
        liquidity_df["Fees Accumulated"][0] = liquidity_df["Fees Accumulated"][0]+fee*price #In terms of Token 1
        print("Total number of transactions: 1")
        print("Total fees accumulated:", liquidity_df["Fees Accumulated"][0], "(In terms of Token 1)")
        return liquidity_df
    
    else:
        raise ValueError("token must take value in [Token 1, Token 2]")


if __name__ == "__main__":

    #Token 1 = $10; Token 2 = $100   => Token 1/Token 2 = 10

    #Simple liquidity pool example
    # $10*1000 Token 1 = 10000; and $100*100 Token 2 = 10000
    # n=1000*100=100000
    #Liquidity curve is Token 1*Token 2 = 100000 = characteristic number
    liq = pd.DataFrame(np.array([1000, 100, 100000, 0.0])).transpose()
    liq.columns = ["Token 1 Supply", "Token 2 Supply", "Char Number", "Fees Accumulated"]

    print(update_liquidity_pool(1, liq, 0.01, token="Token 2"))

    x = np.linspace(1, 1000, 1001)
    y = 100000/x
    fig = px.line(x=x, y=y, labels={"x":"Suppply of Token 2", "y":"Supply of Token 1"})
    fig.show()