# Quantumult X / Clash Rules

自用规则仓库，主要分成三类：

- `gfwlist`: 墙外域名规则
- `proxy`: 默认走代理的常用软件域名
- `local`: 局域网 CIDR 直连规则

## 订阅总览

### Quantumult X

| 规则 | 订阅地址 |
| --- | --- |
| GFW | `https://raw.githubusercontent.com/mrdear/my-clash-rules/main/rules/qx/gfwlist.list` |
| Proxy | `https://raw.githubusercontent.com/mrdear/my-clash-rules/main/rules/qx/proxy.list` |
| Local | `https://raw.githubusercontent.com/mrdear/my-clash-rules/main/rules/qx/local.list` |

### Clash / Mihomo

| 规则 | 订阅地址 | behavior |
| --- | --- | --- |
| GFW | `https://raw.githubusercontent.com/mrdear/my-clash-rules/main/rules/clash/gfwlist.yaml` | `domain` |
| Proxy | `https://raw.githubusercontent.com/mrdear/my-clash-rules/main/rules/clash/proxy.yaml` | `domain` |
| Local | `https://raw.githubusercontent.com/mrdear/my-clash-rules/main/rules/clash/local.yaml` | `ipcidr` |

## 目录结构

- `rules/qx/`: Quantumult X 可直接订阅的规则文件
- `rules/clash/`: Clash / Mihomo 的 rule-provider 文件
- `autoscript/gfw/`: GFW 规则生成脚本
- `autoscript/proxy/`: Proxy 规则生成脚本
- `autoscript/local/`: Local CIDR 规则生成脚本

## 使用示例

### Quantumult X

直接把上面的 `rules/qx/*.list` 地址加入订阅即可。

### Clash / Mihomo

```yaml
rule-providers:
  gfwlist:
    type: http
    behavior: domain
    format: yaml
    url: https://raw.githubusercontent.com/mrdear/my-clash-rules/main/rules/clash/gfwlist.yaml
    path: ./ruleset/gfwlist.yaml
    interval: 86400

  proxy:
    type: http
    behavior: domain
    format: yaml
    url: https://raw.githubusercontent.com/mrdear/my-clash-rules/main/rules/clash/proxy.yaml
    path: ./ruleset/proxy.yaml
    interval: 86400

  local:
    type: http
    behavior: ipcidr
    format: yaml
    url: https://raw.githubusercontent.com/mrdear/my-clash-rules/main/rules/clash/local.yaml
    path: ./ruleset/local.yaml
    interval: 86400
```

```yaml
rules:
  - RULE-SET,local,DIRECT
  - RULE-SET,gfwlist,PROXY
  - RULE-SET,proxy,PROXY
```

## 生成脚本

- `autoscript/gfw/gfwlist_to_quantumultx.py`: 从 GFWList 生成 `gfwlist`
- `autoscript/proxy/proxy_to_quantumultx.py`: 从 Clash 的 `proxy.txt` 生成 `proxy`
- `autoscript/local/local_to_quantumultx.py`: 从 Clash 的 `lancidr.txt` 生成 `local`

## 说明

- `gfwlist` 和 `proxy` 在 Clash 侧都输出为 `behavior: domain` 的 provider payload
- `local` 在 Clash 侧输出为 `behavior: ipcidr` 的 provider payload
- QX 侧的 `local` 会转换为 `IP-CIDR` / `IP-CIDR6` 并直连
