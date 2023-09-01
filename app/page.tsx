"use client";

import { Button, Card, CardBody, Input } from "@nextui-org/react";
import { useState } from "react";

type SharpeRatio = {
  ticker: string;
  annualized_sharpe: number;
  detail?: string;
};
type CalculateBody = {
  ticker: string;
  start_date: string;
  end_date: string;
};
export default function Home() {
  const [SharpeRatio, setSharpeRatio] = useState<SharpeRatio>();
  const [body, setBody] = useState<CalculateBody>({
    ticker: "",
    start_date: "",
    end_date: "",
  });
  const calculate = async () => {
    // send post request to fastapi endpoint
    const response = await fetch("/api/calculate", {
      method: "POST",
      body: JSON.stringify(
        body,
        //   {
        //   ticker: "AAPL",
        //   start_date: "2021-01-01",
        //   end_date: "2021-01-31",
        // }
      ),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    })
      .then(async (res) => {
        const result = await res.json();
        setSharpeRatio(result);
      })
      .catch((err) => console.log(err));
  };
  console.log(SharpeRatio);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-10">
      <div className="z-10 w-full max-w-xl items-center justify-center gap-y-4 font-mono text-sm">
        <div className="p-5 text-center text-xl">
          Stock Performance Calculator
        </div>
        <Card>
          <form
            className="flex flex-col gap-y-2 p-2"
            onSubmit={(e) => {
              e.preventDefault();
              calculate();
            }}
          >
            <Input
              type="text"
              variant={"bordered"}
              label="Ticker"
              placeholder="e.g. AAPL"
              onChange={(e) => {
                setBody({ ...body, ticker: e.target.value });
              }}
            />
            <div className="flex gap-x-2">
              <Input
                type="text"
                variant={"bordered"}
                label="Start Date"
                placeholder="yyyy-mm-dd"
                onChange={(e) => {
                  setBody({ ...body, start_date: e.target.value });
                }}
              />
              <Input
                type="text"
                variant={"bordered"}
                label="End Date"
                placeholder="yyyy-mm-dd"
                onChange={(e) => {
                  setBody({ ...body, end_date: e.target.value });
                }}
              />
            </div>
            <Button
              type="submit"
              color="warning"
              className="hover:bg-warning-600"
            >
              Calculate
            </Button>
          </form>
        </Card>
        {SharpeRatio &&
          (SharpeRatio?.detail !== "Bad Request" ? (
            <Card className="mt-5 border border-warning-400">
              <div>
                <div className="p-5 text-center text-warning-400">
                  {SharpeRatio.ticker}
                </div>
                <div className="px-5 pb-5 text-center">
                  Annualized Sharpe: {SharpeRatio.annualized_sharpe}
                </div>
              </div>
            </Card>
          ) : (
            <div className="mt-2 text-center">Please enter valid fields!</div>
          ))}
      </div>
    </main>
  );
}
