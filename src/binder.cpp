#include <pybind11/pybind11.h>
#include "linefeature_tracker.h"
#include <pybind11/numpy.h> // Include the header for handling numpy arrays
#include <opencv2/opencv.hpp>
#include <iostream>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

// Function to convert a Python cv2 image to cv::Mat
cv::Mat pyarray_to_cv_mat(py::array &py_img) {
    py::buffer_info info = py_img.request();
    int channels = 1;

    if (info.ndim > 2) {
        channels = info.shape[2];
    }

    cv::Mat img(info.shape[0], info.shape[1], CV_8UC(channels), (uint8_t *) info.ptr);

    return img;
}

void bind_Line(py::module &m) {
    py::class_<Line>(m, "Line")
        .def(py::init<>()) // Default constructor
        .def_readwrite("keyPoint", &Line::keyPoint); // Expose keyPoint
}

py::array cv_mat_to_pyarray(const cv::Mat &cpp_img) {
    if (cpp_img.empty()) {
        throw std::runtime_error("Cannot convert empty cv::Mat to a Python array");
    }

    // Create a buffer info for the cv::Mat
    py::array py_img;
    if (cpp_img.channels() == 1) {
        py_img = py::array({ cpp_img.rows, cpp_img.cols }, cpp_img.data);
    } else if (cpp_img.channels() == 3) {
        py_img = py::array_t<uchar>({ cpp_img.rows, cpp_img.cols, cpp_img.channels() }, cpp_img.data);
    } else {
        throw std::runtime_error("Unsupported number of channels in cv::Mat");
    }

    return py_img;
}

// Bindings for FrameLines class
void bind_FrameLines(py::module &m) {
    py::class_<FrameLines, FrameLinesPtr>(m, "FrameLines")
        .def(py::init<>()) // Default constructor

        // Expose member variables (example: 'frame_id', 'img', etc.)
        .def_property_readonly("img", [](FrameLines &self) {
            // Convert cv::Mat img to Python cv2 image (NumPy array)
            return cv_mat_to_pyarray(self.img);
        })
        .def_property_readonly("lineID", [](FrameLines &self) {
            // Return the success vector as a Python list
            py::list lineID_list;
            for (const auto &s : self.lineID) {
                lineID_list.append(s);
            }
            return lineID_list;
        })
        .def_property_readonly("lineRec", [](FrameLines &self) {
            py::list line_rec_list;

            for (const auto &lineRecord : self.lineRec) {
                py::list line_list;
                for (const auto &line : lineRecord) {
                    py::dict line_dict;
                    line_dict["start"] = py::make_tuple((int)line.start.x, (int)line.start.y);
                    line_dict["end"] = py::make_tuple((int)line.end.x, (int)line.end.y);
                    line_list.append(line_dict);
                }
                line_rec_list.append(line_list);
            }

            return line_rec_list;
        })
        .def_property_readonly("vecLine", [](FrameLines &self) {
            py::list line_list; // Create a Python list to hold Line objects

            // Iterate through vecLine and convert each Line to a Python dictionary
            for (const Line &line : self.vecLine) {
                py::dict line_dict;
                // Convert keyPoint to a Python list
                py::list keypoint_list;
                for (const Point2f &point : line.keyPoint) {
                    keypoint_list.append(py::make_tuple((int) point.x, (int) point.y));
                }
                line_dict["keyPoint"] = keypoint_list;
                line_dict["StartPt"] = py::make_tuple((int) line.StartPt.x, (int) line.StartPt.y);
                line_dict["EndPt"] = py::make_tuple((int) line.EndPt.x, (int) line.EndPt.y);
                // Append the dictionary representing the Line to the list
                line_list.append(line_dict);
            }

            return line_list; // Return the list of Line objects
        })
        .def_property_readonly("success", [](FrameLines &self) {
            // Return the success vector as a Python list
            py::list success_list;
            for (const auto &s : self.success) {
                success_list.append(s);
            }
            return success_list;
        });
}



PYBIND11_MODULE(line_tracker, m) {
    m.doc() = R"pbdoc(
        Line Feature Tracker module
        -----------------------
        Module to track lines using Pybind11
    )pbdoc";

    py::class_<LineFeatureTracker>(m, "LineFeatureTracker")
        .def(py::init<>())  // Default constructor
        .def("readImage", [](LineFeatureTracker& self, py::array input, int elsed_bool) {
            // Convert the Python cv2 image to cv::Mat
            cv::Mat image = pyarray_to_cv_mat(input);

            // Call your existing readImage function
            self.readImage(image, elsed_bool);
        }, R"pbdoc(
            Track lines from a Python cv2 image.
        )pbdoc")
        .def("getCurImg", &LineFeatureTracker::getCurImg, "Get cur image from LineFeatureTracker"); 
    bind_Line(m);
    bind_FrameLines(m);
}