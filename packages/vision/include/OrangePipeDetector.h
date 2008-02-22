/*
 * Copyright (C) 2007 Robotics at Maryland
 * Copyright (C) 2007 Daniel Hakim
 * All rights reserved.
 *
 * Author: Daniel Hakim <dhakim@umd.edu>
 * File:  packages/vision/include/OrangePipeDetector.h
 */

#ifndef RAM_ORANGE_PIPE_DETECTOR_H_06_23_2007
#define RAM_ORANGE_PIPE_DETECTOR_H_06_23_2007


// Project Includes
#include "vision/include/Common.h"
#include "vision/include/Detector.h"
#include "core/include/ConfigNode.h"

// Must be included last
#include "vision/include/Export.h"

namespace ram {
namespace vision {
        
class RAM_EXPORT OrangePipeDetector  : public Detector
{
  public:
    bool found;
    OrangePipeDetector(core::ConfigNode config,
                       core::EventHubPtr eventHub = core::EventHubPtr());
    OrangePipeDetector(Camera*);
    ~OrangePipeDetector();
    
    void processImage(Image* input, Image* output= 0);
    
    //get normalized center of line.
    double getX();
    double getY();
    double getAngle();
    void update();

    
    void show(char* window);
    IplImage* getAnalyzedImage();
    
    
  private:
    void init(core::ConfigNode config);
    
    double angle;
    double lineX;
    double lineY;
    IplImage* rotated;
    Image* frame;
    Camera* cam;
};
    
} // namespace vision
} // namespace ram

#endif // RAM_ORANGE_PIPE_DETECTOR_H_06_23_2007

