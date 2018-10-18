package main

import (
	"fmt"
	"os"
	//	"io/ioutil"
	"log"
	"net/http"
	//	"net/http/httputil"
	_ "time"
)

//var url1 string = "https://studygolang.com/articles/12044"

var url1 string = "https://player.vimeo.com/video/272577246"

func check(e error) {
	if e != nil {
		log.Fatal(e)
	}
}
func main() {
	var url string
	b := make([]byte, 100)
	//	var b []byte
	//	fmt.Printf("%v\n", b)

	_, err := fmt.Scanf("%s\n", &url)
	if err != nil {
		log.Fatal(err)
	}
	//		time.Sleep(time.Second)
	fmt.Printf("得到url\n")
	fmt.Printf("%s\n", url)
	response, err := http.Get(url1)
	if err != nil {
		log.Fatal(err)
	}
	defer response.Body.Close()
	file, err := os.Create("test.mp4")
	check(err)
	defer file.Close()
	for {
		n, err := response.Body.Read(b)
		//		fmt.Println("n:", n)
		file.Write(b[:n])
		if err != nil {
			fmt.Printf("over!\n")
			break
		}
	}
	fmt.Printf("exit!\n")
}
