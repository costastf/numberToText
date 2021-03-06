﻿#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: numToText.py
# Copyright (c) 2010 by None
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__  = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '25/06/2010'


import re

class numToText(): 
    def __init__(self, euro=False):
        self.text = ''
        self.euro = euro
        self.singleDigits = (u'μηδέν',u'ένα',u'δύο',u'τρία',u'τέσσερα',u'πέντε',u'έξι',u'επτά',u'οκτώ',u'εννέα')
        self.doubleDigits = (u'δέκα',u'έντεκα',u'δώδεκα')
        self.doubleDigitsplural = (u'τρείς',u'τέσσερις',u'μία')
        self.tenths = (u'δεκα',u'είκοσι',u'τριάντα',u'σαράντα',u'πενήντα',u'εξήντα',u'εβδομήντα',u'ογδόντα',u'εννενήντα')
        self.hundreds = (u'εκατό', u'διακόσια', u'τριακόσια',u'τετρακόσια',u'πεντακόσια',u'εξακόσια',u'επτακόσια',u'οκτακόσια',u'εννιακόσια')
        self.hundredsplural = (u'εκατόν',u'διακόσιες', u'τριακόσιες',u'τετρακόσιες',u'πεντακόσιες',u'εξακόσιες',u'επτακόσιες',u'οκτακόσιες',u'εννιακόσιες')
        self.thousands = (u'χίλια', u'χιλιάδες')
        self.millions = (u'εκατομμύριο', u'εκατομμύρια')
        self.billions = (u'δισεκατομμύριο', u'δισεκατομμύρια')
    def __twoDigits(self, number, thousands=None, hundredFlag=None):
         text = ''
         num = number.zfill(2)
         if num[-1] == '0' and num[-2] == '0':
             text = ''
         elif num[-2] == '0':
             if not thousands:
                 text = self.singleDigits[int(num[-1])]   
             else:
                 if hundredFlag and num[-1] == '1':
                     text = self.doubleDigitsplural[2]   
                 elif num[-1] == '3':
                     text = self.doubleDigitsplural[0]   
                 elif num[-1] == '4':
                     text = self.doubleDigitsplural[1]   
                 else:
                     text = self.singleDigits[int(num[-1])]   
         else:
             if num[-2] == '1' and num[-1] < '3':
                 text = self.doubleDigits[int(num[-1])]
             elif num[-2] == '1' and num[-1] == '3':
                 if thousands:
                     text = u'{0}{1}'.format(self.tenths[0], self.doubleDigitsplural[0])
                 else:
                     text = u'{0}{1}'.format(self.tenths[0], self.singleDigits[int(num[-1])])
             elif num[-2] == '1' and num[-1] == '4':
                 if thousands:
                     text = u'{0}{1}'.format(self.tenths[0], self.doubleDigitsplural[1]) 
                 else:
                     text = u'{0}{1}'.format(self.tenths[0], self.singleDigits[int(num[-1])])
             elif num[-2] == '1' and num[-1] > '4':
                 text = u'{0}{1}'.format(self.tenths[0], self.singleDigits[int(num[-1])])
             elif num[-1] == '0' and num[-2] != '0':
                 text = self.tenths[int(num[-2])-1]
             elif num[-1] != '0' and num[-2] != '0':
                 if not thousands:
                     text = u'{0} {1}'.format(self.tenths[int(num[-2])-1], self.singleDigits[int(num[-1])])
                 else:
                     if num[-2] > '1' and num[-1] == '1':
                         text = u'{0} {1}'.format(self.tenths[int(num[-2])-1], self.doubleDigitsplural[2])
                     elif num[-1] == '3':
                         text = u'{0} {1}'.format(self.tenths[int(num[-2])-1], self.doubleDigitsplural[0]) 
                     elif num[-1] == '4':
                         text = u'{0} {1}'.format(self.tenths[int(num[-2])-1], self.doubleDigitsplural[1]) 
                     else:
                         text = u'{0} {1}'.format(self.tenths[int(num[-2])-1], self.singleDigits[int(num[-1])])
         return text
    def __threeDigits(self, number, thousands=None):
        three = ''
        num = number.zfill(3)
        if thousands:
            if num[-3] == '1':
                two = self.__twoDigits(num[-2:], thousands='True', hundredFlag='True')
            else:
                two = self.__twoDigits(num[-2:], thousands='True')
        else:
            two = self.__twoDigits(num[-2:])
        if not two and num[-3] == '0':
            three = ''
        elif not two and num[-3] != '0':
            if thousands:
                if num[-3] == '1':
                    three = self.hundreds[int(num[-3])-1]
                elif num[-3] > '1':
                    three = self.hundredsplural[int(num[-3])-1]
            else:
                three = self.hundreds[int(num[-3])-1]
        elif num[-3] == '0':
            three = two
        elif num[-3] == '1':
            three = self.hundredsplural[0]+ ' ' + two
        elif num[-3] > '1':
            if thousands:
                three = self.hundredsplural[int(num[-3])-1]+ ' ' + two
            else: 
                three = self.hundreds[int(num[-3])-1]+ ' ' + two
        return three
    def __sixDigits(self,number):
        six = ''
        num = number.zfill(6)
        lastthree = self.__threeDigits(num[-3:])
        firstthree = self.__threeDigits(num[:-3],thousands='True')
        if firstthree:
            if firstthree == u'ένα':
                six = self.thousands[0] + ' ' + lastthree
            else:
                six = firstthree + ' ' + self.thousands[1] + ' ' + lastthree
        else:    
            six = lastthree
        return six
    def __nineDigits(self,number):
        nine = ''
        num = str(number).zfill(9)
        lastsix = self.__sixDigits(num[-6:])      
        firstthree = self.__threeDigits(num[:-6])
        if firstthree:
            if firstthree == u'ένα':
                nine = firstthree + ' ' + self.millions[0] + ' ' + lastsix
            else:
                nine = firstthree + ' ' + self.millions[1] + ' ' + lastsix
        else:    
            nine = lastsix
        return nine
    def __twelveDigits(self,number):
        twelve = ''
        num = str(number).zfill(12)
        lastnine = self.__nineDigits(num[-9:])      
        firstthree = self.__threeDigits(num[:-9])
        if firstthree:
            if firstthree == u'ένα':
                twelve = firstthree + ' ' + self.billions[0] + ' ' + lastnine
            else:
                twelve = firstthree + ' ' + self.billions[1] + ' ' + lastnine
        else:    
            twelve = lastnine
        return twelve
    def getText(self, number):
        decimal = ''
        try:
            fullnumber = str(number).split(',')
            if len(fullnumber) > 2:
                text = u'Παρακαλώ χρησιμοποιήστε το κόμμα για δεκαδικό.\nΔεν επιτρέπονται περισσότερα απο ένα κόμμα στον αριθμό.'
                return text
            integer = re.sub("\D", "", fullnumber[0])
            decimal = re.sub("\D", "", fullnumber[1])
        except:
            pass
        if len(integer) > 12:
            text = u'Η εφαρμογή μπορεί να περιγράψει μέχρι αριθμούς δισεκατομμυρίου.'
            return text	  
        integer = self.__twelveDigits(integer)

        if len(decimal) == 1:
            decimal = str(decimal)+'0'
        decimal = self.__twoDigits(str(decimal)[:2])
        if not integer and not decimal:
            if self.euro:
                text = u'μηδέν ευρώ'
            else:
                text = u'μηδέν'
        elif not integer:
            if decimal == u'ένα':
                if self.euro:
                    text = u'μηδέν ευρώ και ένα λεπτό'
                else:
                    text = u'μηδέν κόμμα μηδέν ένα'
            else:
                if self.euro:
                    text = u'μηδέν ευρώ και {0} λεπτά'.format(decimal)
                else:
                    text = u'μηδέν κόμμα {0}'.format(decimal)                
        elif not decimal:
            if self.euro:
                text = u'{0} ευρώ'.format(integer)
            else:
                text = u'{0}'.format(integer)                
        else:
            if decimal == u'ένα':
                if self.euro:
                    text = u'{0} ευρώ και ένα λεπτό'.format(integer)
                else:
                    text = u'{0} κόμμα μηδέν ένα'.format(integer)                
            else:
                if self.euro:
                    text = u'{0} ευρώ και {1} λεπτά'.format(integer, decimal)
                else:
                    text = u'{0} κόμμα {1}'.format(integer, decimal)                    
        return text

if __name__ == "__main__":
    number = numToText()
    amount = number.getText('5.987,23')
    print(amount)
