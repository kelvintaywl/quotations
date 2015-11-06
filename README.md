# Quotations
[![Build Status](https://travis-ci.org/kelvintaywl/quotations.svg?branch=master)](https://travis-ci.org/kelvintaywl/quotations)


This is a proof of concept for validating quotation marks in text.

Particularly built for translations in mind. See example usage below.


## Usage

```python
from quotations import QuotationValidator

# source in Japanese
source = u"""
「これは最高なものです！」と、彼女は叫びました。
"""

# translation in English
translation = u"""
'This is dog's bollocks!', she exclaimed
"""

# set strict to True; validate quotations from both source and translation
# such that the total qualified quotations from source and translation should tally
# also, the order of quotations will be checked as well
ok, error = QuotationValidator.validate(source, translation, "ja_en", strict=True, verbose=True)
# NOTE: if verbose is False, validate just returns the ok value

try:
    assert ok is True
except AssertionError:
    print(error)
```


## TODO

- [] extend validations for brackets

