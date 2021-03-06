/*
 * Copyright (C) 2007 Robotics at Maryland
 * Copyright (C) 2007 Joseph Lisee <jlisee@umd.edu>
 * All rights reserved.
 *
 * Author: Joseph Lisee <jlisee@umd.edu>
 * File:  packages/core/test/include/MockSubsystem.h
 */

#ifndef RAM_CORE_TEST_MOCKSUBSYSTEM_11_18_2007
#define RAM_CORE_TEST_MOCKSUBSYSTEM_11_18_2007

#include <iostream>

// Project Includes
#include "core/include/Subsystem.h"
#include "core/include/ConfigNode.h"

// Must Be Included last
#include "core/include/Export.h"

class MockSubsystem : public ram::core::Subsystem
{
public:
    MockSubsystem(ram::core::ConfigNode config_, 
                  ram::core::SubsystemList dependents_) :
    	ram::core::Subsystem(config_["name"].asString(), dependents_),
        config(config_),
        dependents(dependents_),
        inBackground(false),
        rate(-1),
        priority(ram::core::IUpdatable::NORMAL_PRIORITY),
        affinity(-1)
    {
    }

    ram::core::ConfigNode config;
    ram::core::SubsystemList dependents;
    bool inBackground;
    int rate;
    IUpdatable::Priority priority;
    int affinity;

    virtual void setPriority(ram::core::IUpdatable::Priority priority_) {
        priority = priority_;
    }
    virtual ram::core::IUpdatable::Priority getPriority() {
        return priority;
    }
    virtual void setAffinity(size_t affinity_) {
        affinity = affinity_;
    };
    virtual int getAffinity() {
        return affinity;
    };
    virtual void update(double) {}
    virtual void background(int rate_) {
        inBackground = true;
        rate = rate_;
    }
    virtual void unbackground(bool) {
        inBackground = false;
    }
    virtual bool backgrounded() {
        return inBackground;
    }
};

#endif // RAM_CORE_TEST_MOCKSUBSYSTEM_11_18_2007
