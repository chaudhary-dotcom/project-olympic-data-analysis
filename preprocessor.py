import pandas as pd

def preprocess(df, region_df):

    #filterning for summer olympics
    df = df[df['Season'] == 'Summer']

    # merger with region_df
    df = df.merge(region_df, on='NOC', how='left')

    # dropping duplicates 
    df.drop_duplicates(inplace=True)

    # one hot encoding 
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df

# if __name__ == "__main__":
#     print(preprocess()) 
