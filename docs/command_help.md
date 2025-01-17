**群聊环境下，同一个群同一个人同一条指令有10秒cd，以期望解决多个机器人相互嵌套的问题**

***因为指令是可以自定义的，因此这里以我自己定义的指令来说明***

**参数介绍: 小括号内的`()`为可选参数，方括号`[]`内的是必选参数，花括号`{}`内的是可用的参数,尖括号`<>`内的是参数类型**

***<font color='gree'>请注意，并不是所有的指令都会列在这里，写的插件越来越多，我也会忘记更新文档，很多指令的用法我一个文档也写不清楚</font>***

### [自定义指令文档](./reg-command_help.md)

---

# 呼出指令面板
```
 help / 帮助    
```
使用 `help`或者`帮助`来呼出指令面板

# 私聊命令

```
ping
```
向服务器ping一下，来验证机器人是否在线

```
addadmin / deladmin qq号
```
分别是 添加机器人管理员 和 删除机器人管理员  **<font color="blue">仅有机器人主人有该权限</font>**

```
getinfo
```

获取机器人当前设置


```
log (level) (num)
```
获取最近 `num` 条的等级为 `level` 的日志 (未完成，以后再去完善)

---

## 系统命令(管理员权限)

```
addblacklist qq号
```
将一个用户添加进黑名单

```
delblacklist qq号
```
将一个用户从黑名单移出

```
stext:: [群号] [文本]
```

向指定群发送文本

```
silence on/true/任意
```
开启全局沉默模式，尽可能减少信息输出,其他参数时为关闭沉默模式

```
norepeat on/true/任意
```
参数为 `on` 或 `true` 时，禁用机器人的复读功能，其他参数为启用复读


----
----

# 群聊命令

## 雀魂相关

**雀魂相关的指令基本都以“ 雀魂”开头，基本格式为 `雀魂xx [参数]`**

### **最重要的指令 `qhpt`**

 ```
qhpt / 雀魂分数 / 雀魂pt [玩家名]  ({3/4})  (index)
 ```

 查询该玩家的雀魂段位分 ( 最后两个参数一般不需要，下面会给出使用实例 )

只有玩家名作为参数时是**模糊查询**，可能会查到多名玩家，继而导致数据库注册有误。**精确查询**请加上对局类型和序号

 **该指令用于向本地数据库注册玩家信息，后面的指令查询雀魂的玩家时都需要先用 qhpt 查一次**

得到的反馈中有查询的玩家与目标玩家不匹配的问题 ( **比如 ID 比较短，刚好是别人的前缀** ) ,会查询到多人

```
#假如是四麻

qhpt 豆本豆豆
```
此时会返回两个人 ( 豆本豆豆 和 豆本豆豆奶奶),而我的目标是前者，可以通过以下指令来获取指定玩家

```
qhpt 豆本豆豆 4 1
# 1 可以省略，默认是取第一个
```
同时，由于该玩家不打三麻，我的默认查询机制是先三麻后四麻。在三麻会查询到一个新的用户 ( 豆本豆豆奶 )，由上可知这不是我的目标玩家。所以会影响我后续的指令匹配。

当`qhpt`指令带后面两个参数( 查询类型 和 查询顺序 )时,可以覆盖之前绑定的用户。

还是以豆本豆豆为例，如果我不小心用普通指令进行查询，玩家匹配错误，可以通过带参数查询来更改绑定的用户

具体的 index ( 查询顺序 ) 请去雀魂牌谱屋搜索

index 是从 `1` 开始的，即 `第一个用户的 index 是 1`

<br>

---

<br>

```
qhsl/雀魂十连 ({限时/常驻}) 
```

来一次模拟雀魂十连，可以在 MajSoulInfo的 [drawcards.yml](../config/MajSoulInfo/drawcards.yml) 中配置哪些装扮或者角色进行up

***我并不清楚雀魂抽卡机制到底是怎么样的，我只是根据它公布的规则的来设计了这个抽卡。十连保底给一个紫礼物，存在绿礼物***

*图一乐就好了，别计较池子里有什么东西了*

*有人说角色爆率偏高,那用猫粮公布的概率抽卡就是这样的*

```
qhgetmyqhsl
```
获取我的抽卡总结

```
qhadd / 雀魂添加关注 [玩家名] 
```

将一个玩家添加至自动查询，有新对局记录时会广播

```
qhgetwatch / 雀魂获取本群关注 
```

获取本群所有的雀魂关注的玩家

```
qhdel / 雀魂删除关注 [玩家名] 
```

将一个玩家从**本群的**自动查询中移除，**不再**在此群自动广播对局该玩家的对局记录

```
qhpaipu / 雀魂最近对局 [玩家名] {3/4} ({1-10})
```

查询一个玩家最近n场3/4人对局记录

```
qhinfo / 雀魂玩家详情 [玩家名] {3/4}  {'基本','立直','血统','更多','all'}
```

查询一个玩家的详细数据

```
qhyb / 雀魂月报 [玩家名] ({3/4}) ([YYYY-m])
```
获取一个玩家某月3/4麻月报，时间格式为 2022-3，可以不带对局类型参数和时间参数，默认为四麻和当前月份

当只有玩家名作为参数时，可以不需要空格，如 `qhybxyshu`


```
qhdisable/enable qhpt/qhsl/qhyb ......
```
禁用 / 启用 该群指令 `qhpt/qhsl/qhyb` 等等指令的使用

----
 <font size=5>Tag相关</font>
```
qhtagon [玩家名] [Tag]
```

在本群内给某个玩家打上Tag，方便将账号和群友进行对应

```
qhtagoff [玩家名] {Tag}
```

当 Tag 给定时，删除 玩家a 的 b Tag

当没有 Tag 时，删除 玩家a的所有Tag

```
qhtaglist {target}
```
返回本群的 <font color="green">玩家名-Tag 表</font>  

当没有指定target的时候，默认输出全部; 

```
例: qhtaglist
```

当 target 存在时，输出 <font color="blue">玩家名 = target</font> 的对应表;

```
例: qhtaglist  xyshu
```

当 target 存在 且 以<font color="red"> tag= </font>或 <font color="red">tagname=</font>开头时(不区分大小写),输出 <font color="blue">Tag = target</font> 的对应表```例: qhtaglist  TaG=NekoRabi```

---

```
freshqh
```

刷新雀魂牌谱信息

---

## 天凤相关

```
thpt / 天凤分数 / 天凤pt   [玩家名] {reset=True}
```
查天凤分数 

该功能存在小问题,无法判断账号分数是否会重置,默认是超过180天就会重置。如果不重置请追加 `reset=false` 

```
thadd [玩家名]
```
添加一个玩家进入天凤对局查询队列，有新对局时会播报

```
thdel [玩家名]
```

将一个玩家从天凤对局查询队列中删除

```
thgetwatch
```
获取本群天凤关注

```
牌理 [牌型文本] # 例如： 114514p1919s810m1z
```

天凤牌理分析 ( 不含国士无双、七对子)

----

## 系统命令

```
silence on/true
```
开启该群的沉默模式，尽可能减少信息输出

其他参数时为关闭改群沉默模式


```
norepeat on/true/任意
```
禁用该群的复读相关功能，尽可能减少信息输出

其他参数时为关闭 ( 即允许复读 )

---

## 其他命令

```markdown
说: [文本]
```
让机器人将文本读出来

```markdown
在[群号]说:[文本]
```

私聊bot，向群聊发送语音

<font color='FF0000'>以上功能需要填写腾讯云密钥</font>

```
转告主人 [文本]
```

在群聊中,别人可以通过发送这段文本，来给bot的主人发消息

**<font color='FF0000'>黑名单用户无法使用此功能 ！</font>**


```
举牌 [内容] 
```

将内容写在举牌小人上发出来，最多支持40个字符

```
亲/亲亲 @群友
```

生成一个互亲的图

*丢、吃、举、逮捕、击杀 等等指令同理*

```
摸/摸摸 @群友
【戳一戳】
```

发送一张摸头图

```
重开 / remake
```

异世界转生模拟

```
bw [文字] [图片]
```
返回一张黑白化的图，并且底部配有文字

```
签到
```

获取1点积分，并抽一张塔罗牌


```
[1-9张]塔罗牌
```

抽x张塔罗牌，返回一个转发消息

```
获取当前积分
```

获取当前积分
```
截图 [<回复消息>]
```

将聊天记录文本进行截图 **只能截图文本**
```
[A]鸡打.
```

发送一段内容主体为A的文字 **( 不要漏掉 '点' `.`)**

```
我超[A].
```
发送一段内容主体为A的文字 **( 不要漏掉 '点' `.`)**

---

仅有机器人管理员有权限控制色图开启

```
open/enable/开启    涩图/色图/setu    
```
在本群开启色图

```
close|disable|关闭   涩图 / 色图 / setu
```
在本群关闭色图

色图两种请求方式

第一种:
```
色图 / 涩图 /setu  (tag)
```
第二种直接写正则了:   `来(\d)*(张|份)([\w\d]+)?\s*(的)?\s*(色图|涩图)\s*$`

简单来说 `来张拉克丝色图`

**<font color='red'>色图功能默认关闭，仅有机器人的管理员可以开启</font>**

***<font color='blue'>色图很容易超时</font>***