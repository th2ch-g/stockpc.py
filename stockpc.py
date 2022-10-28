

import yfinance as yf
import argparse
import sys
import os

home = os.path.expanduser("~")

def arg_parser():
    parser = argparse.ArgumentParser(description = 'Plotter that supports file and pipe input for quick description',
                                     formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument("mode", choices = ["add", "view", "update", "rm", "reset"],
                        help = "Mode")
    parser.add_argument("-n", "--name", type = str, help = "Name of stock")
    parser.add_argument("-t", "--ticker", type = str, help = "Ticker ex.9182, AAPL")
    parser.add_argument("-a", "--amount", type = str, help = "Amount of stock")
    parser.add_argument("-p", "--price", type = str, help = "Price of stock ad purchase")
    parser.add_argument("--path", type = str, default = home + "/.stockpc.tsv", help = "File path to save")
    return parser.parse_args()

# TSV format
# name ticker amount price now_price PASTSUM NOWSUM CHANGES
#                                    SUM     SUM    SUM

def check_file_is_stockpc(args):
    if os.path.isfile(args.path) == False:
        print("[ERROR] File seems not to be existed", file = sys.stderr)
        sys.exit(1)
    with open(args.path) as ref:
        line_number = 0
        for line in ref:
            line_number += 1
            if line_number == 1:
                if line == "# stockpc\n":
                    pass
                else:
                    print("[ERROR] File seems not to be stockpc file",
                          file = sys.stderr)
                    sys.exit(1)
            else:
                break

def view(args):
    check_file_is_stockpc(args)
    PASTSUM_sum = 0
    NOWSUM_sum = 0
    CHANGES_sum = 0
    with open(args.path) as ref:
        line_number = 0
        for line in ref:
            a = line.rstrip().split("\t")
            line_number += 1
            if line_number == 1:
                print("{:>15} {:>15} {:>15} {:>15} {:>15} {:>15} {:>15} {:>15}".format(
                      "name", "ticker", "amount", "price", "now_price",
                      "PASTSUM", "NOWSUM", "CHANGES"), file = sys.stdout)
            else:
                PASTSUM = float(a[2].replace(",", "")) * float(a[3].replace(",",""))
                PASTSUM_sum += PASTSUM
                if len(a) == 5:
                    NOWSUM = float(a[2].replace(",", "")) * float(a[4].replace(",",""))
                    CHANGES = NOWSUM - PASTSUM
                    NOWSUM_sum += NOWSUM
                    CHANGES_sum += CHANGES
                else:
                    NOWSUM = ""
                    CHANGES = ""
                    a.append("")

                print("{:>15} {:>15} {:>15} {:>15} {:>15} {:>15} {:>15} {:>15}".format(
                      a[0], a[1], a[2], a[3], a[4], PASTSUM, NOWSUM, CHANGES), file = sys.stdout)
    print("{:>15} {:>15} {:>15} {:>15} {:>15} {:>15} {:>15} {:>15}".format(
          "", "", "", "", "", PASTSUM_sum, NOWSUM_sum, CHANGES_sum), file = sys.stdout)

def add(args):
    if os.path.isfile(args.path) == False:
        file = open(args.path, "w")
        file.write("# stockpc\n")
    else:
        check_file_is_stockpc(args)
        file = open(args.path, "a")
    file.write("{}\t{}\t{}\t{}\t\t\n".format(
        args.name, args.ticker, args.amount, args.price))
    file.close()
    view(args)

def reset(args):
    check_file_is_stockpc(args)
    os.remove(args.path)

def update(args):
    check_file_is_stockpc(args)
    data = []
    with open(args.path) as ref:
        for line in ref:
            data.append(line.rstrip().split("\t"))
    if len(data) != 0:
        for i in range(1,len(data)):
            ticker_data = yf.download(tickers = data[i][1], period = "1d", interval = "1m")
            ticker_data = ticker_data.tail(1)
            now_price = float(ticker_data["Open"])
            if len(data[i]) != 5:
                data[i].append(now_price)
            else:
                data[i][4] = now_price
    reset(args)
    file = open(args.path, "w")
    file.write("# stockpc\n")
    for i in range(1, len(data)):
        tmp = ""
        for j in range(0, len(data[i])):
            tmp += str(data[i][j])
            tmp += "\t"
        tmp += "\n"
        file.write(tmp)
    file.close()
    view(args)

def rm(args):
    check_file_is_stockpc(args)
    data = []
    with open(args.path) as ref:
        for line in ref:
            if line.split("\t")[0] == args.name:
                continue
            data.append(line)
    reset(args)
    file = open(args.path, "w")
    for i in data:
        file.write(i)
    file.close()

if __name__ == "__main__":
    args = arg_parser()
    if args.mode == "add":
        add(args)
    elif args.mode == "view":
        view(args)
    elif args.mode == "update":
        update(args)
    elif args.mode == "rm":
        rm(args)
    elif args.mode == "reset":
        reset(args)
    else:
        print("[ERROR] not fount mode", file = sys.stderr)
        sys.exit(1)
