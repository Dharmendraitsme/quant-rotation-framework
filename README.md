# NIFTYBEES vs GOLDBEES Rotation Strategy

A Python-based quantitative research project that tests a systematic rotation strategy between NIFTYBEES and GOLDBEES.

## Strategy

The strategy compares the relative strength of NIFTYBEES and GOLDBEES using a rolling lookback period and invests in the stronger asset.

The backtest includes:

- Transaction cost: 0.10%
- Slippage: 0.05%
- Initial capital: ₹100,000
- Lookback: 20 trading days

## Research Process

The project evaluates the strategy through:

1. Data preparation
2. Signal generation
3. Backtesting
4. Performance analysis
5. Trade analysis
6. Benchmark comparison
7. Parameter robustness
8. Out-of-sample validation
9. Walk-forward validation
10. Market regime analysis

## Key Results

| Metric | Rotation Strategy |
|---|---:|
| CAGR | 17.00% |
| Volatility | 36.70% |
| Sharpe Ratio | 0.62 |
| Sortino Ratio | 0.74 |
| Max Drawdown | -33.18% |
| Profit Factor | 2.23 |
| Win Rate | 56.74% |

The strategy is compared against NIFTYBEES, GOLDBEES, and a 50/50 benchmark.

## Project Structure

```text
quant-rotation-framework/
│
├── data/raw/          # Input market data
├── results/            # Performance results and charts
├── src/                # Research modules
├── tests/              # Testing
├── main.py             # Main research pipeline
├── requirements.txt    # Python dependencies
└── README.md