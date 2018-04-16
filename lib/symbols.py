import os

static_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'static')

rh_crypto_file = 'rh_crypto.txt'
rh_etf_file = 'rh_etfs.txt'
nasdaq_file = 'nasdaqlisted.txt'
snp_file = 'snp.txt'


def load_symbol_file(f):
    """Reads a plaintext symbol file where each line has a different sym."""
    syms = []
    with open(os.path.join(static_dir, f), 'r') as infile:
        syms = list(map(lambda x: x.strip(), infile.readlines()))

    return syms


RH_CRYPTO = load_symbol_file(rh_crypto_file)
RH_ETF = load_symbol_file(rh_etf_file)
NASDAQ = load_symbol_file(nasdaq_file)
SNP = load_symbol_file(snp_file)
