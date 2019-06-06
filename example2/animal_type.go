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
