//首先利用statik工具将静态文件夹生成对应的go包
//命令为statik -src=文件路径

package main

import (
	"fmt"
	"image/jpeg"
	"image/png"
	"net/http"
	"path"

	_ "statik" //引入由statik生成的静态文件go包

	"github.com/rakyll/statik/fs"
)

func main() {
	statikFS, err := fs.New()
	if err != nil {
		log.Fatal(err)
	}
	go func() {
		http.Handle("/Data/", http.StripPrefix("/Data/", http.FileServer(statikFS)))
		http.ListenAndServe(":8080", nil)
	}()
	im, err := LoadImagByHttp("http://localhost:8080/Data/小黑.png")
	if err != nil {
		log.Fatal(err)
	}
	// do something for im
}

func LoadImagByHttp(url string) (img image.Image, err error) {
	r, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}
	defer r.Body.Close()
	if suffix := path.Ext(url); suffix == ".png" {
		img, err = png.Decode(r.Body)
	} else if suffix == ".jpg" || suffix == ".jpeg" {
		img, err = jpeg.Decode(r.Body)
	} else {
		fmt.Printf("找不到正确的图标")
	}
	return img, err
}
