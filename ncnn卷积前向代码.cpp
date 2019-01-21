#include <stdio.h>
#include <algorithm>
#include <vector>
#include "net.h"
#include <ctime>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>


static int classifier(const ncnn::Net& net,const cv::Mat& bgr, std::vector<float>& pre){

    float* pin;
    unsigned char* pin2;
    ncnn::Mat in;
    ncnn::Mat out;
   // std::cout << bgr.rows<<" "<<bgr.cols <<" "<<bgr.size<<"\n";
    cv::Mat mv[3];
    split(bgr, mv);
//    in = ncnn::Mat::from_pixels_resize(bgr.data,ncnn::Mat::PIXEL_RGB,bgr.cols,bgr.rows,in_w,in_h);
    in = ncnn::Mat::from_pixels(mv[0].data,ncnn::Mat::PIXEL_GRAY,bgr.cols,bgr.rows);
    // for(int i =0;i<28*28;i++){
    //     printf("%dth: %d\n",i,in.data[i]);
    // }
    //printf("in ok!\n");
    // in.to_pixels(im.data,ncnn::Mat::PIXEL_GRAY);

    // cv::imshow("image", bgr);
    // cv::waitKey(0);
    //in.reshape(in.w*in.h*in.c);


    // pin = (float*)in.data;
    
    // pin2 = (unsigned char*) bgr.data;
    // for(int j = 0;j<28;j++){
    //     if(j<10)
    //         printf(" %d ",j);
    //     else
    //         printf("%d ",j);
    //     for(int i =0; i<28;i++){
    //         if(mv[0].data[j*28+i]>127)
    //             printf("1");
    //         else
    //             printf("0");
    //         //printf("%u ",pin2[j*28+i]);
    //     }
    //     printf("\n");
    // }
 //   const float mean_vals[3] = {0.5f, 0.5f, 0.5f};
 //   const float norm_vals[3] = {0.007843f, 0.007843f, 0.007843f};
 //   in.substract_mean_normalize(0, norm_vals);
 //   in.substract_mean_normalize(mean_vals, 0);
    //printf("\n");
    std::cout << in.w<<" "<<in.h <<" "<<in.c<<"\n";
    ncnn::Extractor ex = net.create_extractor();
    //ex.set_light_mode(true);
    //ex.set_num_threads(4);
    ex.input("data",in);
    //printf("extract begin!\n");
    ex.extract("dense2_fwd",out);
    //printf("out ok!\n");
    //ncnn::Mat out_flatterned = out.reshape(out.w*out.h*out.c);
    //printf("out flatterned ok!\n");
    pre.resize(out.w);
    //printf("pre resize ok!\n");
    for(int j =0; j<out.w;j++){
        pre[j] = out[j];
        //printf("pre %d is %.3f\n",j,pre[j]);
    }
    // cv::Mat image(in_h,in_w,CV_8UC3,in.data);
    // cv::Mat mv[3];
    // cv::imshow("image", image);
    // cv::waitKey(0);
    // cv::imshow("image1", bgr);
    // split(bgr, mv);
    // cv::imshow("image2", mv[0]);
    // printf("w: %d, h: %d     w: %d, h： %d", image.cols, image.rows, bgr.cols, bgr.rows);
     
    return 0;
}
static int print_topk(const std::vector<float>& cls_scores, int topk)
{
    // partial sort topk with index
    int size = cls_scores.size();
    std::vector< std::pair<float, int> > vec;
    vec.resize(size);
    for (int i=0; i<size; i++)
    {
        vec[i] = std::make_pair(cls_scores[i], i);
    }

    std::partial_sort(vec.begin(), vec.begin() + topk, vec.end(),
                      std::greater< std::pair<float, int> >());

    // print topk and score
    for (int i=0; i<topk; i++)
    {
        float score = vec[i].first;
        int index = vec[i].second;
        fprintf(stderr, "%d = %f\n", index, score);
    }

    return 0;
}
void print_result(std::vector<float>& scores){
    //auto maxPosition = std::max_element(scores.begin(),scores.end());
    std::vector<float>::iterator maxPosition = std::max_element(scores.begin(),scores.end());
    //std::cout<<*maxPosition<<std::endl ;
    std::cout<<"图中数字是："<< maxPosition-scores.begin()<<std::endl ;
}
int main(int argc,char** argv)
{
    if(argc !=2)
        {
            fprintf(stderr,"Usage: %s [imagepath]\n",argv[0]);
            return -1;
        }

    const char* imagepath = argv[1];

    cv::Mat m = cv::imread(imagepath,CV_LOAD_IMAGE_COLOR);

    if(m.empty())
    {
        fprintf(stderr,"cv::imread %s failed\n",imagepath);
        return -1;
    }
    ncnn::Net mlp;
    mlp.load_param("mylenet.param");
    mlp.load_model("mylenet.bin");
    std::vector<float> cls_scores;
    clock_t begin = clock();
    classifier(mlp,m,cls_scores);
    clock_t End = clock();
    //print_topk(cls_scores,3);
    print_result(cls_scores);
    
    double duration = double(End-begin)/CLOCKS_PER_SEC;
    printf("识别时长：%f\n",duration);
    printf("OK!\n");

    //cv::waitKey(0);

}