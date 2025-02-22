package main

import (
	"fmt"
	"os"

	"github.com/ahenrie/UBA/util"
)

func main() {
	fmt.Println("############### Start Parsing logs ###############")
	util.ProcessLogFile(os.Args[1], os.Args[2])
}
