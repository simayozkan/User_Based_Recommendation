import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

book_tags = pd.read_csv("/Users/simayozkan/Desktop/ds/archive(4)/book_tags.csv")

books = pd.read_csv("/Users/simayozkan/Desktop/ds/archive(4)/books.csv")

ratings = pd.read_csv("/Users/simayozkan/Desktop/ds/archive(4)/ratings.csv")

sample_book = pd.read_xml("/Users/simayozkan/Desktop/ds/archive(4)/sample_book.xml")

tags = pd.read_csv("/Users/simayozkan/Desktop/ds/archive(4)/tags.csv")

to_read = pd.read_csv("/Users/simayozkan/Desktop/ds/archive(4)/to_read.csv")

ratings.head()


user_df = df.groupby(["user_id","title"])["rating"].mean().unstack()
user_df
259
random_user = user_df.sample(1,random_state=689).index[0]

random_user_df = user_df[user_df.index == random_user]

book_read = random_user_df.dropna(axis=1).columns.tolist()

book_read_df = user_df[book_read]

user_book_count = book_read_df.T.notnull().sum()

users_same_books = user_book_count[user_book_count > (book_read_df.shape[1] * 30 ) / 100].index

df_ = book_read_df[book_read_df.index.isin(users_same_books)]

corr_df = df_.T.corr().unstack().drop_duplicates()

top_readers = pd.DataFrame(corr_df[random_user][corr_df[random_user] > 0.75], columns=["corr"])
top_readers

top_readers_ratings = pd.merge(top_readers, df[["user_id", "book_id", "rating"]], how='inner', on="user_id")
top_readers_ratings

top_readers_ratings['weighted_rating'] = top_readers_ratings['corr'] * top_readers_ratings['rating']
top_readers_ratings

recommendation_df = top_readers_ratings.pivot_table(values="weighted_rating", index="book_id", aggfunc="mean")
recommendation_df.head()

books_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.0].sort_values(by="weighted_rating", ascending=False).head()
books_recommend

books[books["book_id"].isin(books_recommend.index)]


