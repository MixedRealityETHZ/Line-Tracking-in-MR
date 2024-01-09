#include <iostream>
#include "linefeature_tracker.h"
#include "ELSED.h"
#define VIS_TRACK false
#include <opencv2/ximgproc.hpp>

int main() {
    LineFeatureTracker trackerData;

    cv::Mat frame1, frame2;
    int pub_count = 1;
    
    VideoCapture capture("../tests/testvideo.mp4");
    Mat frame;

    if( !capture.isOpened() )
        throw "Error when reading steam_avi";
    
    capture >> frame; // Read the first frame
    if (frame.empty())
        throw "Error reading the first frame";

    //cv::VideoWriter outputVideo = cv::VideoWriter("output_video.avi", cv::VideoWriter::fourcc('M', 'J', 'P', 'G'),\
    // 30, cv::Size(frame.cols, frame.rows));
    
    int elsed_bool = 0;
    int frame_count = 0;
    std::chrono::steady_clock::time_point start, end;

    start = std::chrono::steady_clock::now();

    //Per frame detection
    Ptr<cv::ximgproc::EdgeDrawing> ed = cv::ximgproc::createEdgeDrawing();
    upm::ELSED elsed;

    double min_edline_length = 0.125;

    if (elsed_bool){
        upm::ELSEDParams params;
        params.gradientThreshold = 32;
        params.anchorThreshold = 16;
        params.scanIntervals = 2;
        params.minLineLen = min_edline_length * (std::min(frame.cols, frame.rows));

        elsed.setParams(params);
    } else{
        ed->params.EdgeDetectionOperator = cv::ximgproc::EdgeDrawing::SOBEL;
        ed->params.GradientThresholdValue = 32;
        ed->params.AnchorThresholdValue = 16;
        ed->params.ScanInterval = 2;
        ed->params.MinLineLength = min_edline_length * (std::min(frame.cols, frame.rows));
    }

    // Main loop to process video frames
    for (;;)
    {
        cv::Mat img;
        cv::cvtColor(frame, img, cv::COLOR_BGR2GRAY);
        vector<Vec4f> edlines;
        if (elsed_bool){
            edlines = elsed.detect(img);
        } else {
            ed->detectEdges(img); ed->detectLines(edlines);
        }

        // Draw detected lines on the frame
        for (const auto &line : edlines)
        {
            // Extract line coordinates
            Point pt1(line[0], line[1]);
            Point pt2(line[2], line[3]);

            // Draw the line on the frame (assuming 'frame' is a color image)
            cv::line(frame, pt1, pt2, Scalar(0, 255, 0), 2, LINE_AA); // Green lines with thickness 2
        }

        // Save the processed frame as an image
        //string output_frame_path = "frames/frame_" + to_string(frame_count) + ".jpg";
        // imwrite(output_frame_path, frame);

        frame_count++;

        cv::imshow("img", frame);
        cv::waitKey(1);

        // Continue capturing frames
        capture >> frame;

        // Break the loop if the frame is empty
        //outputVideo.write(frame);
        if (frame.empty())
            break;
    }

    // Release the video capture
    capture.release();
    end = std::chrono::steady_clock::now();

    std::chrono::duration<double> elapsed_time = end - start;
    std::cout << frame_count << std::endl;
    std::cout << frame_count / elapsed_time.count() << std::endl;
    exit(EXIT_FAILURE);

    for( ; ; )
    {
        trackerData.readImage(frame, elsed_bool);

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
            
            cv::line(frame, start, end, cv::Scalar(0, 255, 0), 2, LINE_AA);
            cv::line(frame, start1, end1, cv::Scalar(0, 255, 0), 1, LINE_AA);
            cv::putText(frame, std::to_string(trackerData.cur_img->lineID[j]), trackerData.cur_img->vecLine[j].keyPoint[0], cv::FONT_HERSHEY_SIMPLEX, 0.45, CV_RGB(255, 230, 0), 1.8);
        }
        for (unsigned int m = 0; m < trackerData.cur_img->vecLine.size(); m++)
        {
            if (trackerData.cur_img->success[m] == -1)
                break;

            Point2f start = un_lines[m].keyPoint[1];
            Point2f end = un_lines[m].keyPoint[un_lines[m].keyPoint.size() - 1];
            Point2f start1 = un_lines[m].StartPt;
            Point2f end1 = un_lines[m].EndPt;
            
            cv::line(frame, start, end, cv::Scalar(0, 0, 255), 2, LINE_AA);
            cv::line(frame, start1, end1, cv::Scalar(0, 0, 255), 1, LINE_AA);
            cv::putText(frame, std::to_string(trackerData.cur_img->lineID[m]), trackerData.cur_img->vecLine[m].keyPoint[0], cv::FONT_HERSHEY_SIMPLEX, 0.45, CV_RGB(255, 230, 0), 1.8);
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
                        cv::line(frame, start, end, cv::Scalar(0, 255, 0), 2, LINE_AA);
                    else
                        cv::line(frame, start, end, cv::Scalar(0, 0, 55 + 10*j), 1, LINE_AA);
                }
            }
        }
        
        cv::imshow("img", frame);
        cv::waitKey(1);
        //outputVideo.write(frame);
        frame_count++;
        capture >> frame;

        if(frame.empty())
            break;
    }

    end = std::chrono::steady_clock::now();

    std::chrono::duration<double> elapsed_seconds = end - start;

    std::cout << frame_count / elapsed_seconds.count() << std::endl;

    //outputVideo.release();
    waitKey(0);

    return 0;
}
