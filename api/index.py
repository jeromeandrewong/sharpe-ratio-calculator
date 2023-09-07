from fastapi import FastAPI, HTTPException
import numpy as np
from pydantic import BaseModel
import pandas as pd
import yfinance as yf

app = FastAPI()


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}


class StockInput(BaseModel):
    # ticker is a string array
    ticker: str
    start_date: str
    end_date: str


@app.post("/api/calculate")
def calculate(input: StockInput):
    try:
        ticker = input.ticker
        start_date = input.start_date
        end_date = input.end_date
        risk_free_rate = 0.02

        # extracting data from yfinance
        prices_df = yf.download(ticker, start=start_date, end=end_date)

        # convert datatime index to date format
        prices_df.index = prices_df.index.date

        # keep adjusted close
        prices_df = pd.DataFrame(prices_df[["Adj Close"]])

        # create returns dataframe
        returns_df = prices_df.pct_change()

        # calculate daily returns as geometric mean
        returns_per_day = (returns_df + 1).prod() ** (1 / returns_df.shape[0]) - 1

        # calculate annualized volatility
        annualized_vol = returns_df.std() * np.sqrt(252)

        # calculate annualized returns
        annualized_returns = (returns_per_day + 1) ** 252 - 1

        # calculate sharpe ratio
        sharpe_ratio = (annualized_returns - risk_free_rate) / annualized_vol

        return {
            "ticker": ticker,
            "annualized_sharpe": sharpe_ratio["Adj Close"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=("Bad Request"))
