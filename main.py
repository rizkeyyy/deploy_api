from fastapi import FastAPI, HTTPException, Header
import pandas as pd
from pydantic import BaseModel
# create instance/object
app = FastAPI()

#define API_KEY
apiKey = "kucingoren123"

#base_url/domain

# define endpoint home
@app.get("/")
def first_home():
    return {"message": "Selamat datang di HCK-023!"}

#define endpoint protected
@app.get("/protected")
def root(key: str = Header(None)):
    #cek api_key
    if key == None or key != apiKey:
        raise HTTPException(status_code=401, detail="Key yang anda masukan tidak sesuai!")

# define endpoint data
@app.get("/data")
def get_data():
    # read data from csv file
    df = pd.read_csv("data.csv")

    # convert dataframe to dictionary
    return df.to_dict(orient='records')

@app.get("/data/{id}")
def get_data_by_id(id: int):
    # read data from csv file
    df = pd.read_csv("data.csv")

    # opsi untuk filtering -> df[kondisi] atau df.query(kondisi)
    # opsi untuk manggil kolom -> df['id'] atau df.id

    # filter berdasarkan id
    filter = df[df.id == id]
    
    # condition if-else for filtering
    # if our data is not found or there is no match data
    if len(filter) == 0:
        # return pesan error
        raise HTTPException(status_code=404, detail='Data nggak ada bro! :( Sabar ya')
    
    # if our data is found
    else:
        # convert dataframe to dictionary
        return filter.to_dict(orient='records')
    
# Endpoint for searching by name
@app.get("/data/name/{fullname}")
def get_data_by_name(full_name: str):
    # read data from csv file
    df = pd.read_csv("data.csv")
    
    # case-insensitive search for the name
    filter_name = df[df.fullname.str.lower() == full_name.lower()]
    
    # if our data is not found or there is no match data
    if len(filter_name) == 0:
        # return pesan error
        raise HTTPException(status_code=404, detail='Namanya nggak ada bro! :(')
    
    # if our data is found
    return filter_name.to_dict(orient='records')


class DataInput(BaseModel):
    fullname: str
    email: str

# define endpoint for updating data
@app.post('/input_data/')
def add_data(update_df:dict):

    df = pd.read_csv('data.csv')

    # define new id for new data
    id = len(df) + 1

    #assign new id to column id in new df named update_df 
    update_df['id'] = id

    # create new dataframe because we will use concat
    new_data = pd.DataFrame([update_df])

    # concat dataframe
    df = pd.concat([df, new_data], ignore_index=True)

    # Save updated DataFrame back to CSV
    df.to_csv('data.csv', index=False)

    return df.to_dict(orient='records')

