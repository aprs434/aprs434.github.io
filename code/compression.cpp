/*

C++ codec algorithms for APRS 434 LoRa:

    - Callsign Compression CCCC
    - SSID, pathCode & Data Type Compression D

    - Callsign Compression EEEE
    - SSID & MessageNo Compression F

    - Text Compression tttt


REVISION HISTORY

    2022-05-11 PA0FOT Initial version and tests


REQUIRES
    $ sudo apt install libboost-all-dev


CAVEAT ON ESP32

    Avoid deep recursive function calls.
    Individual recursive function calls do not always add a lot of stack usage each time they are called,
    but if each function includes large stack-based variables then the overhead can get quite high.

    https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/performance/ram-usage.html


CAVEAT LARGEST INTEGER

    The largest unsigned integer produced by this algorithm is:
    In [1]: 42**51
    Out[1]: 61053956130164410003966197248726664261467607807747252759217406888527859374733918208

*/

// #define DEBUG

#define uchar unsigned char
#define uint unsigned int

#include <assert.h>
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cctype>
#include <cmath>
#include <boost/multiprecision/cpp_dec_float.hpp>
#include <boost/multiprecision/cpp_int.hpp>

namespace mp = boost::multiprecision;
using std::cout;
using std::endl;
using std::dec;
using std::oct;
using std::hex;

const char* digits = " -./0123456789?@ABCDEFGHIJKLMNOPQRSTUVWXYZ";

mp::uint512_t bignum;
uchar bytes[100];

uchar* encodeBase(int n, mp::uint512_t num) {     // base n, unsigned num - 64 bytes max

    int i, nummodn;

    assert(n <= strlen(digits));
    assert (n > 1);

    i = 0;
    while (num > 0) {
        nummodn = (int)(num % n);
        bytes[i++] = digits[nummodn];
        num /= n;
    };
    bytes[i] = 0;
    strrev((char*)bytes);

    return bytes;                                 // return base n encoded '\0' terminated string
}

mp::uint512_t decodeBase(int b, char* str) {      // base b, str 64 bytes max '\0' terminated

    mp::uint512_t result;
    mp::uint512_t weight;
    int i, j, k, ch;

    assert(b <= strlen(digits));
    assert (b > 1);

    result = 0, weight = 1;
    for (i = j = strlen(str); i > 0; i--)         // iterate over input string
    {
        ch=toupper(str[i-1]);
        for (k = 0; k < strlen(digits); k++) {    //lookup char index
            if (digits[k] == ch) {
                break;
            }
        }
        if (k == strlen(digits))                  // ignore if ch not found in digits
            continue;
        result = result + ((k) * weight);
        weight = weight * b;
    }

    return result;                                // result can be pow(42,51)!
}

uint encodeCCCC(std::string s) {
    return (uint)decodeBase(36, (char*)s.c_str());
}

uchar* decodeCCCC(uint i) {
    return encodeBase(36, i);
}

mp::uint512_t encodetttt(std::string s) {
    return decodeBase(42, (char*)s.c_str());
}

uchar* decodetttt(mp::uint512_t i) {
    return encodeBase(42, i);
}

int main() {

    char uncompressed[] = "0 This is ON4AA-6. QSL? @ Yes/No";
    char challenge[100];

    int i;

    printf("%08x\n", encodeCCCC("PA0FOT"));
    printf("%s\n\n", decodeCCCC(encodeCCCC("PA0FOT")));

    printf("%08x\n", encodeCCCC("pa3fkm"));
    printf("%s\n\n", decodeCCCC(encodeCCCC("pa3fkm")));

    printf("%08x\n", encodeCCCC("ON4AA"));
    printf("%s\n\n", decodeCCCC(encodeCCCC("ON4AA")));

    printf("%08x\n", encodeCCCC("W3A"));
    printf("%s\n\n", decodeCCCC(encodeCCCC("W3A")));

    printf("%08x\n", encodeCCCC("0HN0"));
    printf("%s\n\n", decodeCCCC(encodeCCCC("0HN0")));

    bignum = encodetttt((char*) uncompressed);
    cout << hex << bignum << " = " << dec << sizeof(bignum) << " bytes" << endl;
    decodetttt(bignum);
    cout << bytes << " =  " << strlen((char*)bytes) << " bytes" << endl;


    while (1) {
        printf("\nEnter text for testing, or press enter to exit\n");
        printf("-> ");
        i = 0;
        while(i<sizeof(challenge)-1) {
            scanf("%c", &challenge[i]);
            if (challenge[i] == '\n')
                break;
            i++;
            }
        challenge[i]='\0';

        if (i == 0)
            break;

        cout << "challenge: '" << challenge << "' - " << strlen(challenge) << " bytes" << endl;
        cout << "encoded  : " << hex << (bignum = encodetttt(challenge)) << endl;
        decodetttt(bignum);
        cout << "decoded  : '" << bytes << "' - " << strlen((char*)bytes) << " bytes" << endl << endl;
    }

    return 0;
}
