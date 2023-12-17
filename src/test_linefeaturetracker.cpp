#include <iostream>
#include "linefeature_tracker.h"
#define VIS_TRACK false

int main() {
    LineFeatureTracker trackerData;

    cv::Mat frame1, frame2;
    int pub_count = 1;
    
    VideoCapture capture("../tests/test_video3.mp4");
    Mat frame;

    if( !capture.isOpened() )
        throw "Error when reading steam_avi";
    
    capture >> frame; // Read the first frame
    if (frame.empty())
        throw "Error reading the first frame";

    cv::VideoWriter outputVideo = cv::VideoWriter("output_video.avi", cv::VideoWriter::fourcc('M', 'J', 'P', 'G'),\
     30, cv::Size(frame.cols, frame.rows));
    
    int elsed = 0;

    for( ; ; )
    {
        trackerData.readImage(frame, elsed);

        cv::Mat tmp_img;
        cv::cvtColor(trackerData.cur_img->img, tmp_img, CV_GRAY2RGB);

        const vector<Line> &un_lines = trackerData.cur_img->vecLine;
        for (unsigned int j = 0; j < trackerData.cur_img->vecLine.size(); j++)
        {
            if (trackerData.cur_img->success[j] != -1)
                continue;

            Point2f start = un_lines[j].keyPoint[1];
            Point2f end = un_lines[j].keyPoint[un_lines[j].keyPoint.size() - 1];
            Point2f start1 = un_lines[j].StartPt;
            Point2f end1 = un_lines[j].EndPt;
            
            cv::line(tmp_img, start, end, cv::Scalar(0, 255, 0), 2, LINE_AA);
            cv::line(tmp_img, start1, end1, cv::Scalar(0, 255, 0), 1, LINE_AA);
            cv::putText(tmp_img, std::to_string(trackerData.cur_img->lineID[j]), trackerData.cur_img->vecLine[j].keyPoint[0], cv::FONT_HERSHEY_SIMPLEX, 0.45, CV_RGB(255, 230, 0), 1.8);
        }
        for (unsigned int m = 0; m < trackerData.cur_img->vecLine.size(); m++)
        {
            if (trackerData.cur_img->success[m] == -1)
                break;

            Point2f start = un_lines[m].keyPoint[1];
            Point2f end = un_lines[m].keyPoint[un_lines[m].keyPoint.size() - 1];
            Point2f start1 = un_lines[m].StartPt;
            Point2f end1 = un_lines[m].EndPt;
            
            cv::line(tmp_img, start, end, cv::Scalar(255, 0, 0), 2, LINE_AA);
            cv::line(tmp_img, start1, end1, cv::Scalar(255, 0, 0), 1, LINE_AA);
            cv::putText(tmp_img, std::to_string(trackerData.cur_img->lineID[m]), trackerData.cur_img->vecLine[m].keyPoint[0], cv::FONT_HERSHEY_SIMPLEX, 0.45, CV_RGB(255, 230, 0), 1.8);
        }

        cv::Mat detect_img;
        cv::cvtColor(trackerData.cur_img->img, detect_img, CV_GRAY2RGB);

        if (VIS_TRACK){
            LineRecord lines;

            for (unsigned int m = 0; m < trackerData.cur_img->lineRec.size(); m++){
                lines = trackerData.cur_img->lineRec[m];
                if (lines.size() > 20) lines.erase(lines.begin(), lines.end() - 20);
                
                for (unsigned int j = 0; j < lines.size(); j++)
                {
                    Point2f start = lines[j].start;
                    Point2f end = lines[j].end;
                    if (j == lines.size() - 1)
                        cv::line(detect_img, start, end, cv::Scalar(0, 255, 0), 2, LINE_AA);
                    else
                        cv::line(detect_img, start, end, cv::Scalar(0, 0, 55 + 10*j), 1, LINE_AA);
                }
            }
            cv::imshow("img", detect_img);
            cv::waitKey(20);
            outputVideo.write(detect_img);
        } else{
            cv::imshow("img", tmp_img);
            cv::waitKey(20);
            outputVideo.write(tmp_img);
        }
        capture >> frame;

        if(frame.empty())
            break;
    }

    outputVideo.release();
    waitKey(0);

    return 0;
}