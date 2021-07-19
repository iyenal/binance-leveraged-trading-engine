# IDTS Blitztrader - (Binance) Leveraged Trading Engine
For algorithmic trading

Python engine for trading on cross and isolated leveraged margin - focus on operability and optimisation for fast (<100ms) and reliable trades.
Based on the excellent python-binance for orders execution (API management) and used in production environnement.

## Features

- Quantity tracking
- Support for fees
- Efficient API calls
- Protection against overruns
- Status restoration with %store
- Currently used

### Support for fees and quantity to use (Important!)

Binance trading fees management being weird on isolated margin balances, it's recommended to let some tokens on the ALT sub-balance so fees can be correctly covered.
Binance will first take fees from these tokens, then if BNB discount is enabled, take them from your **Spot BNB Balance** and refund them in the next hour in your according pair's isolated margin balance.
So the script especially for shorts will not margin sell immediately all your ALT balance, but will borrow what asked.
In resume, your isolated margin balance should look like this:

Pair's balance for a **100% quantity in ALT unit**:
ALT: ~10% for fees
BTC/USDT: 100% for trade + ~10% for fees

### Example on a BUSDUSDT pair:

Quantity: **100 BUSD** (in script)
Isolated margin balance:
**ALT (BUSD): 10 BUSD
USDT: 110 USDT**
Resume: For every position it'll take 100 BUSD as qty, and so use 100 USDT on the USDT balance as 1 BUSD ~= 1 USDT (simple example as these are stable coins).
In case of ALTS, if the balance isn't enough for the position and it's a LONG for example, it'll borrow what's needed to make the trade (eg 0.5 BUSD ~= 1 USDT so it'll borrow 100 USDT to make a 100 BUSD position) hence the leveraged nature. **Be cautionous with liquidation risks that put in danger your collateral.**

### Protection against calls overrun

Every pair position can only be opened if one isn't yet, and can only be closed if one has been opened with the according position.
Eg. closing a SHORT trade on BTCUSDT is only posible if a SHORT trade has been previously opened on BTCUSDT (and so the margin sell order has been succesfully executed, otherwise exceptions handling would be triggered, and that wouldn't allow the trade opening registration).

### Status retrieval

All the open positions are stored in the history_trades array at every change, which are stored in disk using the %store magic.
That variable being retrieved at every script restart to allow the protection against overruns being operable even if the script got restarted for whatever reason.
If the environnement doesn't support %store magic, according lines can be commented safely but will disable that feature.

### Issues and pull requests

Keep issues only for issues, and pull requests for worthy and optimized improvements.
I can't warranty that I'll read them in a timely manner.

### Licence

![WDDTH](https://en.meming.world/images/en/thumb/a/a3/We_Don%27t_Do_That_Here.jpg/300px-We_Don%27t_Do_That_Here.jpg)

## Donate

Donations are always appreciated, feel free to send BNBs:
BEP20(BSC) 0x74da82bdafa31baf6814b7d322a46a781c80626b

## Advices and warranty notices

No warranty is given and no responsability is held by the usage of this script.
Trading is a risky activity, in an environnement full of sharks, making it a financial activity.
Leveraging your positions on volatile markets such as crypto can lead to serious losses.

Always backtest roughfully and keep consistent your strategies, trade responsibly whan you can afford to lose.
You wouldn't like to end up with no money https://www.youtube.com/watch?v=xUVz4nRmxn4
