numberToText
============

A class for translating numbers to their equivalent greek text. The instantiation of the class can get an argument of "euro" set to true if one wants the text to be expressed as euro amount.

The usage is very simple 

```
    number = numToText()
    amount = number.getText('5.987,23')
    print(amount)
    

returns : πέντε χιλιάδες εννιακόσια ογδόντα επτά κόμμα είκοσι τρία

    number = numToText(euro=True)
    amount = number.getText('5.987,23')
    print(amount)
    

returns : πέντε χιλιάδες εννιακόσια ογδόντα επτά ευρώ και είκοσι τρία λεπτά
```

The thousands delimiter is not important and can be ommited. The decimal delimiter is the comma (,) as per the greek standard.
So the numbers 32654,23 32.654,23 are the same. One could even input 3.2.6.5.4,2.3 and it would be the same. Of course there can not be more than one decimal delimiter. So the number 32,654,23 is invalid and wouldn't translate with a helpfull error message.
Have fun!
