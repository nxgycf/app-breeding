
create database if not exists breeding;
use breeding;

create table if not exists admin(
id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
account VARCHAR(32) NOT NULL comment '账号',
password VARCHAR(32) NOT NULL comment '密码',
name VARCHAR(32) NOT NULL DEFAULT '',
level INTEGER NOT NULL DEFAULT 1,
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间'
)AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists user_info(
id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT comment '用户ID',
account VARCHAR(32) NOT NULL comment '账号',
phone VARCHAR(16) NOT NULL DEFAULT '' comment '手机号码',
nickname VARCHAR(16) NOT NULL DEFAULT '' comment '昵称',
password VARCHAR(32) NOT NULL comment '密码',
avatar_id BIGINT NOT NULL DEFAULT 0 comment '头像ID',
deliver_address_id BIGINT NOT NULL DEFAULT 0 comment '默认邮寄地址id',
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
INDEX (account,phone),
UNIQUE (account)
)AUTO_INCREMENT=100000 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists wechat_user(
id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT comment '用户ID',
openid VARCHAR(32) NOT NULL comment '账号',
nickname VARCHAR(16) NOT NULL DEFAULT '' comment '昵称',
sex TINYINT NOT NULL DEFAULT 0 comment '状态（0：未知，1：man，2：woman）',
province VARCHAR(16) NOT NULL DEFAULT '' comment '省',
city VARCHAR(16) NOT NULL DEFAULT '' comment '市',
country VARCHAR(16) NOT NULL DEFAULT '' comment '国家',
headimgurl VARCHAR(128) NOT NULL DEFAULT '' comment '头像',
deliver_address_id BIGINT NOT NULL DEFAULT 0 comment '默认邮寄地址id',
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
INDEX (openid),
UNIQUE (openid)
)AUTO_INCREMENT=100000 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists user_goods(
id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT comment '订单ID',
code VARCHAR(18) NOT NULL comment '订单号',
transaction_id VARCHAR(32) NOT NULL DEFAULT '' comment '微信交易ID',
user_id BIGINT NOT NULL comment 'user ID',
goods_id INTEGER NOT NULL comment 'goods ID',
goods_name VARCHAR(16) NOT NULL DEFAULT '' comment '商品名称',
goods_price FLOAT NOT NULL comment '价格,单位:元',
number INTEGER NOT NULL DEFAULT 1 comment '数量',
amount FLOAT NOT NULL comment '金额',
feed_day INTEGER NOT NULL DEFAULT 0 comment '喂养/种植 时长,单位:day',
deliver_date TIMESTAMP NOT NULL comment '发货时间',
status TINYINT NOT NULL DEFAULT 0 comment '状态（0:待支付，1：喂养中/种植中/准备中，2：已发货，3：已完成）',
deliver_address_id BIGINT NOT NULL DEFAULT 0 comment '默认邮寄地址id',
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
INDEX (user_id,goods_id, deliver_date, code, transaction_id),
UNIQUE (code, transaction_id)
)AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists user_deliver_address(
id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_id BIGINT NOT NULL comment 'user ID',
name VARCHAR(16) NOT NULL DEFAULT '' comment '收货人姓名',
phone VARCHAR(16) NOT NULL DEFAULT '' comment '收货人手机号码',
address VARCHAR(256) NOT NULL DEFAULT '' comment '详细地址',
zip_code INTEGER NOT NULL DEFAULT 0 comment '邮政编码',
region_id INTEGER NOT NULL DEFAULT 0 comment '地区ID',
region_name VARCHAR(128) NOT NULL DEFAULT '' comment '地区',
status TINYINT NOT NULL DEFAULT 1 comment '1：正常，0：删除',
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
INDEX (user_id,status)
)AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists user_pay(
id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_goods_id BIGINT NOT NULL comment '订单号',
transaction_id VARCHAR(32) NOT NULL DEFAULT '' comment '微信交易ID',
user_id BIGINT NOT NULL comment 'user ID',
goods_id INTEGER NOT NULL comment '商品id',
pay_type TINYINT NOT NULL DEFAULT 1 comment '支付类型（1：微信，2：支付宝）',
amount FLOAT NOT NULL comment '金额',
status TINYINT NOT NULL comment '状态（0：失败，1：成功）',
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
INDEX (user_goods_id,user_id,goods_id,transaction_id),
UNIQUE (user_goods_id, transaction_id)
)AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists deliver_info(
id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_goods_id BIGINT NOT NULL comment '订单号',
user_id BIGINT NOT NULL comment 'user ID',
goods_id INTEGER NOT NULL comment '商品id',
goods_name VARCHAR(16) NOT NULL DEFAULT '' comment '商品名称',
number INTEGER NOT NULL DEFAULT 1 comment '数量',
express_name VARCHAR(16) NOT NULL comment '快递公司名称',
express_no VARCHAR(32) NOT NULL comment '快递号',
status TINYINT NOT NULL comment '状态（0：发货中，1：已完成）',
deliver_address_id BIGINT NOT NULL DEFAULT 0 comment '默认邮寄地址id',
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
INDEX (user_goods_id,user_id,goods_id, create_date),
UNIQUE (user_goods_id)
)AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists user_news(
id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
user_id BIGINT NOT NULL comment 'user ID',
content VARCHAR(128) NOT NULL DEFAULT '' comment '消息内容',
status TINYINT NOT NULL DEFAULT 0 comment '状态(1：已阅读，0：未阅读)',  
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
INDEX (user_id)
)AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists goods_info(
id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
code INTEGER NOT NULL comment '商品编号',
avatar_id BIGINT NOT NULL DEFAULT 0 comment '头像ID',
name VARCHAR(16) NOT NULL comment '名字',
price FLOAT NOT NULL comment '价格,单位:元',
type SMALLINT NOT NULL DEFAULT 1 comment '类别,1:养殖类,2:果蔬类,3:谷物类',
feed_day INTEGER NOT NULL DEFAULT 0 comment '喂养/种植 时长,单位:day',
brief VARCHAR(128) NOT NULL DEFAULT '' comment '简介',
number INTEGER NOT NULL DEFAULT 1 comment '剩余数量',
detail VARCHAR(512) NOT NULL DEFAULT '' comment '描述',
status TINYINT NOT NULL DEFAULT 0 comment '状态（0：正常，1：下架）',
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
INDEX (code, type, status),
UNIQUE (code)
)AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists avatar_info(
id BIGINT NOT NULL PRIMARY KEY,
filename VARCHAR(32) NOT NULL comment '文件名称',
type TINYINT NOT NULL DEFAULT 0 comment '文件类型',
path VARCHAR(128) NOT NULL DEFAULT '' comment '存放路径（绝对路径）',
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
)AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists goods_picture(
id BIGINT NOT NULL PRIMARY KEY,
goods_id INTEGER NOT NULL comment '商品id',
filename VARCHAR(32) NOT NULL comment '文件名称',
type TINYINT NOT NULL DEFAULT 0 comment '文件类型,0:普通图片,1:详细图片',
path VARCHAR(128) NOT NULL DEFAULT '' comment '存放路径（绝对路径）',
create_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP comment '创建时间',
update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
INDEX (goods_id, type)
)AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8;

//new
CREATE TABLE IF NOT EXISTS region(
id INTEGER NOT NULL PRIMARY KEY,
region_code VARCHAR(8) NOT NULL COMMENT '地区编码',
region_name VARCHAR(32) NOT NULL DEFAULT '' comment '地区名字',
region_level TINYINT NOT NULL DEFAULT 0 comment '级别',
city_code VARCHAR(6) NOT NULL DEFAULT '' comment '区号',
center VARCHAR(32) NOT NULL DEFAULT '' COMMENT '城市中心点（即：经纬度坐标）',
parent_id INTEGER NOT NULL DEFAULT -1 comment '父级ID',
INDEX (parent_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='地区码表';

//old
create table if not exists region(
id INTEGER NOT NULL PRIMARY KEY,
region_name VARCHAR(64) NOT NULL DEFAULT '' comment '地区名字',
parent_region_id INTEGER NOT NULL DEFAULT 0 comment '父级ID',
region_level TINYINT NOT NULL DEFAULT 0 comment '级别',
region_desc VARCHAR(64) DEFAULT '' comment '地区描述',
status TINYINT NOT NULL DEFAULT 0 comment '状态',
region_phone_code VARCHAR(6) NOT NULL DEFAULT '' comment '区号',
region_pinyin VARCHAR(64) NOT NULL DEFAULT '' comment '拼音',
region_english VARCHAR(64) NOT NULL DEFAULT '' comment 'English',
is_default TINYINT NOT NULL DEFAULT 0 comment '',
first_letter VARCHAR(16) NOT NULL DEFAULT '' comment '首写字母',
zip_code VARCHAR(8) DEFAULT '' comment 'zip code',
bd_city VARCHAR(8) DEFAULT '' comment '',
INDEX (parent_region_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
