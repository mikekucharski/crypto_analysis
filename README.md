# crypto_analysis

Implementation and cryptanalysis of simple ciphers. 

# How to use

**Note:** run from the root directory of the repo
```
// Encrypt/decrypt using cipher module
python run.py -c hill -m "abcd" -k "2.2.2.3" encrypt

// Run cryptanalysis tool
python -m pyciph.vigenere_cipher.vigenere_breaker

// Run all tests
python -m unittest discover

// Run tests for single cipher
python -m unittest discover -s pyciph.hill_cipher
```