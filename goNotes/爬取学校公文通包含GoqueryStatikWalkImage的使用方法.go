package main

import (
	"bufio"
	"fmt"
	"image"
	"image/jpeg"
	"image/png"
	"io"
	"io/ioutil"
	"log"
	//	"net/http"
	_ "net/http/httputil"
	"os"
	"path"
	"regexp"
	//	"strconv"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/lxn/walk"
	. "github.com/lxn/walk/declarative"
	"golang.org/x/net/html/charset"
	"golang.org/x/text/encoding"
	"golang.org/x/text/transform"
)
import (
	"net/http"

	_ "statik"

	"github.com/rakyll/statik/fs"
)

var url string = "https://www1.szu.edu.cn/board/"
var debug bool = false

func checkErr(e error) {
	if e != nil {
		fmt.Printf("error!")
		log.Fatal(e)
	}
}

//type MyResponse http.Response

var sourceString string = `<td align="center" style="font-size: 9pt"><a href=# onclick="document.fsearch1.search_type.value='fu';document.fsearch1.keyword.value='信息工程学院';document.fsearch1.dayy.value=.*?;document.fsearch1.searchb1.click\(\);">信息工程学院</a></td>[^<]*<td>[^<]*<a target=_blank href="(.*?)" class=fontcolor3>`

func main() {
	/*static files operations*/
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
	/*task for gui*/
	var outTE *walk.TextEdit
	var mw *walk.MainWindow
	//	im, err := LoadImag("./wang.jpg")
	//	im, err := LoadImag("./小黑.png")
	//	if err != nil {
	//		fmt.Print("png open error!")
	//	}
	icon, err := walk.NewIconFromImage(im)
	MainWindow{
		AssignTo: &mw,
		Title:    "一个都不能少",
		Name:     "gwt",
		Enabled:  true,
		Visible:  true,
		//		Size:     Size{600, 200},
		MinSize: Size{400, 100},
		Layout:  VBox{},
		Children: []Widget{
			TextEdit{AssignTo: &outTE, ReadOnly: false},
			//				outTE.SetText("lkjlkjl " + strconv.Itoa(j))
		},
		Icon: icon,
	}.Create()

	/*task for spider*/
	go func() {
		for {
			ids, titles, ReTimes, departments := GetIdsTitleTime(url)

			for i, id := range ids {
				//		content := GetContentFromTargetUrl(url + id)
				//		fmt.Println(content)
				func() {
					var out string = ""
					doc := GetUtf8DocumentFromUrl(url + id)
					//			checkErr()
					doc.Find("p").Each(func(i int, selection *goquery.Selection) {
						out += selection.Text()
					})

					outTE.SetText(ReTimes[i] + " " + departments[i] + ":" + titles[i])
				}()
				time.Sleep(8 * time.Second)
			}
		}
	}()

	go GetIdsTitleTime(url)
	mw.Run()
}

func GetIdsAndTitle(url string) ([]string, []string) {
	var reExpression string
	client := &http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	checkErr(err)
	req.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36")
	response, err := client.Do(req)
	checkErr(err)
	defer response.Body.Close()
	//	ResPrint(response)
	encode := determinEncoding(response.Body)
	utf8Reader := transform.NewReader(response.Body, encode.NewDecoder())
	//	r1, err := httputil.DumpResponse(response, true)

	r, err := ioutil.ReadAll(utf8Reader)
	checkErr(err)

	re, err := regexp.Compile(sourceString)
	checkErr(err)
	all_id := re.FindAllStringSubmatch(string(r[:]), -1)
	ids := make([]string, len(all_id))
	titles := make([]string, len(all_id))
	//	re_times := make([]string, len(all_id))
	for i, matches := range all_id {
		//		fmt.Println(matches[1])
		ids[i] = matches[1]
		reExpression = `<a target=_blank href="` + ids[i][:8] + `\?` + ids[i][9:] + `" class=fontcolor3>·<b><font color=black>(.*?)</font></b></a>` //.*?([0-9]{4}-[0-9]{1,2}-[0-9]{1-2})</td>
		reTitle, err := regexp.Compile(reExpression)
		checkErr(err)
		title_matches := reTitle.FindAllStringSubmatch(string(r[:]), -1)
		if 0 != len(title_matches) {
			titles[i] = title_matches[0][1] //因为id号是唯一的，所以只能检索出一个，故可以直接使用title_matches[0]
			//			re_times[i] = title_matches[0][2]
		} else {
			reExpression = `<a target=_blank href="` + ids[i][:8] + `\?` + ids[i][9:] + `" class=fontcolor3>.(.*?)</a>` //.*?([0-9]{4}-[0-9]{1,2}-[0-9]{1-2})</td>
			reTitle, err := regexp.Compile(reExpression)
			checkErr(err)
			title_matches := reTitle.FindAllStringSubmatch(string(r[:]), -1)

			titles[i] = title_matches[0][1] //因为id号是唯一的，所以只能检索出一个，故可以直接使用title_matches[0]
			//			re_times[i] = title_matches[0][2]
		}

	}
	return ids, titles
}

func GetIdsTitleTime(url string) ([]string, []string, []string, []string) {
	utf8doc := GetUtf8DocumentFromUrl(url)
	//	targetContent
	//	ids := make([]string, 1000)
	var departments []string
	var ids []string
	var reTimes []string
	var titles []string
	utf8doc.Find("tr[bgcolor=\"#FFFFFF\"]").Each(func(i int, selection *goquery.Selection) {

		selection.Find("a[href=\"#\"]").Each(func(j int, s *goquery.Selection) {
			if s.Text() == "信息工程学院" {

				departments = append(departments, s.Text())
				/*找到子网址*/
				href, _ := selection.Find("a[target=\"_blank\"][class=\"fontcolor3\"]").Attr("href")
				//				href, _ := selection.Find(".fontcolor3").Attr("href")
				ids = append(ids, href)
				/*找到title*/
				titles = append(titles, selection.Find("a[target=\"_blank\"][class=\"fontcolor3\"]").Text())
				/*找到时间*/
				selection.Find("td[align=\"center\"][style=\"font-size: 9pt\"]").Each(func(k int, st *goquery.Selection) {
					if k == 2 {
						reTimes = append(reTimes, st.Text())
					}

				})
				//

			}

		})

	})
	if debug {
		fmt.Println(ids)
		for _, v := range titles {

			fmt.Println(v)
		}
		fmt.Println(reTimes)
	}
	return ids, titles, reTimes, departments
}
func GetContentFromTargetUrl(suburl string) string {
	var out string = ""
	doc := GetUtf8DocumentFromUrl(suburl)
	doc.Find("p").Each(func(i int, selection *goquery.Selection) {
		out += selection.Text()
	})
	return out
}
func ResPrint(this *http.Response) {
	fmt.Printf("Status:%s\n", this.Status)
	fmt.Printf("StatusCode:%d\n", this.StatusCode)
	fmt.Printf("Proto:%s\n", this.Proto)
	//	fmt.Printf("Header:%s\n", this.Header)
}

func determinEncoding(r io.Reader) encoding.Encoding {
	bytes, err := bufio.NewReader(r).Peek(1024)
	checkErr(err)
	e, _, _ := charset.DetermineEncoding(bytes, "")
	return e
}

func GetUtf8DocumentFromUrl(Url string) *goquery.Document {
	res, err := http.Get(Url)
	checkErr(err)
	defer res.Body.Close()
	encode := determinEncoding(res.Body)
	utf8Reader := transform.NewReader(res.Body, encode.NewDecoder())
	r, err := ioutil.ReadAll(utf8Reader)
	checkErr(err)
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(r[:])))
	if err != nil {
		log.Fatal(err)
	}
	return doc
}

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
