# 数据源元信息

## 字段
### 短文本
xShortText

基本类型： string

用来存储标识信息，最大长度不可超过256。可以用来建立索引。
### 长文本
xLongText

基本类型： string

用来存储描述信息。最大长度不可超过64k。
### 普通数字
xNumber

基本类型： number
### 时间戳
xTimestamp

基本类型： number

unix时间戳，ms级别。
### 图片
xPicture

基本类型： string

存储url
### 文件
xFile

基本类型： string

存储url
### 关联关系
#### 多对一关联关系
xManyToOne

基本类型： string
#### 一对多关联关系
xOneToMany

基本类型： string
