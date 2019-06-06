# easy2code

Easy to generate repetitive code from schemas。

在写代码的时候，会遇到一些重复性的代码，可能我们昨天在写，今天在写，明天还在写这些代码。
为了避免这种无意义的劳动，一种方式就是生成这些重复性的代码。  

重复性的代码里包含 `变的代码` 和 `不变的代码` （都是不变的代码的话….那只能祈求上天了）  

`不变的代码` 可以提取出来成为 `模版文件(Template File)`  
`变的代码` 可以当成参数提取出来，在 easy2code，这些参数提取到一个文件，这个文件称为 `实例文件(Instance File)`。  

easy2code 可以根据 `模版文件` 和 `实例文件` 生成 `代码文件(Code File)`，代码文件里就包含了所谓的重复性代码.

## 文件类型

easy2code 包含三种文件：  
模版文件(Template File): 使用模版语言 [Jinja2](http://docs.jinkan.org/docs/jinja2/)  
实例文件(Instance File): 支持 [json5](https://json5.org/)  
代码文件(Code File): 生成的代码所在的文件  

## installation

~~download a binary from our release page:
[TODO](https://github.com/ForeverEnjoy/easy2code/tree/master)~~

1. download the project from [here](https://github.com/ForeverEnjoy/easy2code/tree/master)

2. add `${easy2code-path}/dist` to `PATH`

## usage

```bash
easy2code [-t template_file] [-i instance_file] [-c code_file]

# instance-file 支持目录或单个文件, 比如 a.tmpl, ./dog/ 等
# code-file 支持使用固定名称或者使用 instance-file 里声明的变量， 比如 a.json5, ./{{name}}.go

# 生成单个文件
easy2code -t enum.tmpl -i animal_type.json5 -c ./animal_type.go

# 多个 instace 文件
easy2code -t enum.tmpl -i ./ -c ./{{name}}.go # code-file 支持使用 instace-file 里的变量
```

## example

### enum.tmpl (template-file)

```js
{% with -%}

package {{ name }}

import "strings"

{% set type_name = name | pascalcase  %}
type Enum{{type_name}} uint64


const (
{% for e in enums %}
    {{ e.name | pascalcase }} Enum{{type_name}} = {{ e.value -}}
{% endfor %}
)

var (
	EnumNameToValue map[string]uint64 = make(map[string]uint64)
	ValueToEnumName map[uint64]string = make(map[uint64]string)
)

func init() {
{% for e in enums %}
    EnumNameToValue["{{ e.name | upper }}"] = {{ e.value -}}
{% endfor %}
{% for e in enums %}
    ValueToEnumName[{{ e.value }}] = {{ e.name | upper -}}
{% endfor %}
}

{%- endwith %}
```

### animal_type.json5 (instance-file)

```js
{
    name : "animal_type",
    enums : [
        {
            name : "cat",
            value : 1
        },
        {
            name : "dog",
            value : 2
        },
        {
            name: "rabbit",
            value: 3
        }
    ]
}
```

通过 template-file 和 instance-file 生成 code-file
```shell
> easy2code -t enum.tmpl -i animal_type.json5 -c ./animal_type.go
```

### animal_type.go (Code File)
```golang
package animal_type

import "strings"


type EnumAnimalType uint64


const (

    Cat EnumAnimalType = 1
    Dog EnumAnimalType = 2
    Rabbit EnumAnimalType = 3
)

var (
	EnumNameToValue map[string]uint64 = make(map[string]uint64)
	ValueToEnumName map[uint64]string = make(map[uint64]string)
)

func init() {

    EnumNameToValue["CAT"] = 1
    EnumNameToValue["DOG"] = 2
    EnumNameToValue["RABBIT"] = 3

    ValueToEnumName[1] = CAT
    ValueToEnumName[2] = DOG
    ValueToEnumName[3] = RABBIT
}
```

## 模版内置函数

1. **underscore** 把字符串中的空格和`-`替换为 `_`  
2. **pascalcase** 把字符串转换为 pascal case  
3. **camelcase** 把字符串转换为 camel case
