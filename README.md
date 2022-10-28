# stockpc.py
stock price checler with CLI

## Install
~~~sh
git clone https://github.com/th2ch-g/stockpc.py.git && \
cd stockpc.py && \
sed -e "1i#\!$(which python3)" -i stockpc.py
~~~

### Dependencies
- yfinance
- argparse
- sys
- os

## Usage
~~~
$ stockpc.py add -n shosenmitsui1 -t 9104.T -a 100 -p 2800
      name     ticker     amount      price  now_price    PASTSUM     NOWSUM    CHANGES
shosenmitsui1     9104.T        100       2800              280000.0
                                                         280000.0          0          0
$ stockpc.py view
           name          ticker          amount           price       now_price         PASTSUM          NOWSUM         CHANGES
  shosenmitsui1          9104.T             100            2800          2888.0        280000.0        288800.0          8800.0
                                                                                       280000.0        288800.0          8800.0
$ stockpc.py update
[*********************100%***********************]  1 of 1 completed
           name          ticker          amount           price       now_price         PASTSUM          NOWSUM         CHANGES
  shosenmitsui1          9104.T             100            2800          2888.0        280000.0        288800.0          8800.0
                                                                                       280000.0        288800.0          8800.0
$ stockpc.py rm -n shosenmitsui1
(delete only line named "shosenmitsui1")
$ stockpc.py reset
(same as rm -f $HOME/stockpc.tsv)
~~~



