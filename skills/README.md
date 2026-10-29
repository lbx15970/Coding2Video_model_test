# 互联网 Skill 登记

引入外部 skill（GitHub / 官方市场 / 本 IDE 商店）时，按下面规则落盘并登记。

## 目录约定

```
skills/
├── registry.yaml          # 总表：来源、版本、license、用途、调用方式
├── README.md              # 本文件
└── <skill_name>/          # 实际代码/说明，目录名用 skill 原名
```

## 登记字段

- `name`：skill 原名
- `source`：原始 URL（必须可回溯）
- `version` / `commit`：锁定版本，避免上游漂移
- `license`：确认可商用
- `used_in_cases`：被哪些用例引用
- `entry`：调用入口（脚本路径 / 命令 / prompt 片段）
- `risk`：是否联网、是否执行任意代码、是否上传客户素材（客户素材出域需先确认）

## 安全底线

- 客户提供的素材视为敏感数据，任何会外发到第三方的 skill 先在 `risk` 字段标明并单独确认。
- skill 代码入库前扫一遍 `curl`/`requests`/`exec`/`eval`，确认没有回传。
