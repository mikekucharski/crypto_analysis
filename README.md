# crypto_analysis
Implementation and analysis of historical cipher and modern day encryptions methods

## Run encryption method
```python run.py -c hill -m "abcd" -k "2.2.2.3" encrypt```

## RUn cryptanalysis tool
```python -m mycrypto.vigenere.vigenere_breaker```

## Run all tests from root directory
```python -m unittest discover```

## Run specific cipher tests
```python -m unittest discover -s mycrypto.hill```