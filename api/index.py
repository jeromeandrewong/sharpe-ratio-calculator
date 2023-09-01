from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StockInput(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    # TODO:
    # interval


@app.post("/api/calculate")
def calculate(input: StockInput):
    try:
        ticker = input.ticker
        start_date = input.start_date
        end_date = input.end_date

        # download historical data
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

        # Calculate daily returns
        data["Daily_Returns"] = data["Adj Close"].pct_change()

        # Calculate mean return and standard deviation
        mean_return = data["Daily_Returns"].mean()
        std_deviation = data["Daily_Returns"].std()

        # Assuming a risk-free rate of 2%
        risk_free_rate = 0.02

        # Calculate Sharpe ratio
        sharpe_ratio = (mean_return - risk_free_rate) / std_deviation

        # Annualize Sharpe ratio
        annualized_sharpe = sharpe_ratio * (252**0.5)

        return {
            "ticker": ticker,
            "annualized_sharpe": annualized_sharpe,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=("Bad Request"))
