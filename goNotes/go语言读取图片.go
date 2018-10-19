
import (
	"fmt"
	"image/jpeg"
	"image/png"
	"path"
)
import (
	"net/http"

	_ "statik"

	"github.com/rakyll/statik/fs"
)

func LoadImag(path_ string) (img image.Image, err error) {
	file, err := os.Open(path_)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	if suffix := path.Ext(path_); suffix == ".png" {
		img, err = png.Decode(file)
	} else if suffix == ".jpg" || suffix == ".jpeg" {
		img, err = jpeg.Decode(file)
	} else {
		fmt.Printf("找不到正确的图标")
	}

	return
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