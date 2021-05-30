# CTF HackTheBox 2021 Cyber Apocalypse 2021 - passphrase

Category: Reversing, Points: 300

![info.JPG](https://user-images.githubusercontent.com/30731432/120116735-d8fbe800-c189-11eb-944a-7519b1c3e6ac.png)

Attached file: [passphrase](passphrase)

# passphrase Solution

Let's run the attached binary:

```console
┌─[natyk@kali]─[/htb/cyber_apocalypse/rev/passphrase]
└──╼ $ ./passphrase 

Halt! ⛔
You do not look familiar..
Tell me the secret passphrase: 111111

Intruder alert! 🚨

```

Si on le lance avec Ltrace on peut voir un ```strcmp``` qui compare l'entrée a "3xtr4t3rR3stR14L5_VS_hum4n5" :

```console
┌─[natyk@kali]─[/htb/cyber_apocalypse/rev/passphrase]
└──╼ $ ./passphrase 
...
strlen("\nTell me the secret passphrase: "...)                                                         = 32
sleep(1)                                                                                               = 0
fgets(1111
"1111\n", 40, 0x7fabbddae980)                                                                    = 0x7ffd317aedf0
strlen("1111\n")                                                                                       = 5
strcmp("3xtr4t3rR3stR14L5_VS_hum4n5", "1111")                                                          = 2
printf("\033[31m")                                                                                     = 5
strlen("\nIntruder alert! \360\237\232\250\n")                                                         = 22                                                            
putchar(10, 0x7ffd317ac750, 0x559e2f98ec17, 7                                                                                                                          
)                                   
...
```
On peut donc en déduire que le flag est ```CHTB{3xtr4t3rR3stR14L5_VS_hum4n}```.
