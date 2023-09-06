from fastapi import FastAPI, HTTPException
import numpy as np
from pydantic import BaseModel

# from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import yfinance as yf

app = FastAPI()


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


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

        data = yf.download(ticker, start=start_date, end=end_date)["Adj Close"]

        daily_returns = data.pct_change().dropna()

        mean = daily_returns.mean()

        daily_std = daily_returns.std()

        cum_returns = data[-1] / data[0] - 1

        annualised_std = daily_std * np.sqrt(252)

        # assuming risk free rate of 2%
        rfr = 0.02

        sharpe_i = (cum_returns - rfr) / annualised_std

        return {
            "ticker": ticker,
            "annualized_sharpe": sharpe_i,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=("Bad Request"))
