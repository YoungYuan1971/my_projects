window = global;
const JSEncrypt = require("jsencrypt");
const CryptoJS = require("crypto-js");

// 参数加密
var paramPublicKey =
    "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCvxXa98E1uWXnBzXkS2yHUfnBM6n3PCwLdfIox03T91joBvjtoDqiQ5x3tTOfpHs3LtiqMMEafls6b0YWtgB1dse1W5m+FpeusVkCOkQxB4SZDH6tuerIknnmB/Hsq5wgEkIvO5Pff9biig6AyoAkdWpSek/1/B7zYIepYY0lxKQIDAQAB";
var encrypt = new JSEncrypt();
encrypt.setPublicKey(paramPublicKey);

var b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var b64pad = "=";
function hex2b64(h) {
    var i;
    var c;
    var ret = "";
    for (i = 0; i + 3 <= h.length; i += 3) {
        c = parseInt(h.substring(i, i + 3), 16);
        ret += b64map.charAt(c >> 6) + b64map.charAt(c & 63);
    }
    if (i + 1 == h.length) {
        c = parseInt(h.substring(i, i + 1), 16);
        ret += b64map.charAt(c << 2);
    } else if (i + 2 == h.length) {
        c = parseInt(h.substring(i, i + 2), 16);
        ret += b64map.charAt(c >> 2) + b64map.charAt((c & 3) << 4);
    }
    while ((ret.length & 3) > 0) {
        ret += b64pad;
    }
    return ret;
}

JSEncrypt.prototype.encryptUnicodeLong = function (string) {
    var k = this.getKey();
    //根据key所能编码的最大长度来定分段长度。key size - 11：11字节随机padding使每次加密结果都不同。
    var maxLength = ((k.n.bitLength() + 7) >> 3) - 11;
    try {
        var subStr = "",
            encryptedString = "";
        var subStart = 0,
            subEnd = 0;
        var bitLen = 0,
            tmpPoint = 0;
        for (var i = 0, len = string.length; i < len; i++) {
            //js 是使用 Unicode 编码的，每个字符所占用的字节数不同
            var charCode = string.charCodeAt(i);
            if (charCode <= 0x007f) {
                bitLen += 1;
            } else if (charCode <= 0x07ff) {
                bitLen += 2;
            } else if (charCode <= 0xffff) {
                bitLen += 3;
            } else {
                bitLen += 4;
            }
            //字节数到达上限，获取子字符串加密并追加到总字符串后。更新下一个字符串起始位置及字节计算。
            if (bitLen > maxLength) {
                subStr = string.substring(subStart, subEnd);
                encryptedString += k.encrypt(subStr);
                subStart = subEnd;
                bitLen = bitLen - tmpPoint;
            } else {
                subEnd = i;
                tmpPoint = bitLen;
            }
        }
        subStr = string.substring(subStart, len);
        encryptedString += k.encrypt(subStr);
        return hex2b64(encryptedString);
    } catch (ex) {
        return false;
    }
};

function dataTojson(a) {
    var b = [];
    var c = {};
    b = a.split("&");
    for (var i = 0; i < b.length; i++) {
        if (b[i].indexOf("=") != -1) {
            var d = b[i].split("=");
            if (d.length == 2) {
                c[d[0]] = d[1];
            } else {
                c[d[0]] = "";
            }
        } else {
            c[b[i]] = "";
        }
    }
    return c;
}

function sort_ASCII(a) {
    var b = new Array();
    var c = 0;
    for (var i in a) {
        b[c] = i;
        c++;
    }
    var d = b.sort();
    var e = {};
    for (var i in d) {
        e[d[i]] = a[d[i]];
    }
    return e;
}

function getUuid() {
    var s = [];
    var a = "0123456789abcdef";
    for (var i = 0; i < 32; i++) {
        s[i] = a.substr(Math.floor(Math.random() * 0x10), 1);
    }
    s[14] = "4";
    s[19] = a.substr((s[19] & 0x3) | 0x8, 1);
    s[8] = s[13] = s[18] = s[23];
    var b = s.join("");
    return b;
}

function encryptData(b) {
    var c = Date.parse(new Date());
    var d = getUuid();
    var e = JSON.stringify(sort_ASCII(dataTojson(b || "{}")));
    b = encrypt.encryptUnicodeLong(e);
    var f = CryptoJS.MD5(e + d + c).toString();
    return {
        timestamp: c,
        requestId: d,
        sign: f,
        payload: b,
    };
}

// params = "page=1&limit=20";
// console.log(encryptData(params));

// 数据解密
function decryptData(a) {
    var key = "3583ec0257e2f4c8195eec7410ff1619",
        iv = "d93c0d5ec6352f20";
    var b = CryptoJS.enc.Utf8.parse(key);
    var c = CryptoJS.enc.Utf8.parse(iv);
    var d = CryptoJS.AES.decrypt(a, b, {
        iv: c,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
    });
    return d.toString(CryptoJS.enc.Utf8);
}

// var a =
//     "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";

// console.log(decryptData(a));
