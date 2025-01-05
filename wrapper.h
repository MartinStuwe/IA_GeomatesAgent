#include <box2d/box2d.h>

#ifndef __WRAPPER_H__
#define __WRAPPER_H__
typedef struct bodyElem {
    b2BodyId b2Body;
    int ref;
    void *next;
} bodyElem;

typedef struct bodyPose {
    b2Vec2 position;
    float rotation;
    float size;
} bodyPose;


void initWorld(float gx, float gy);
void destroyWorld(void);
void initPlayers(float rx, float ry, float rs, float rd, float rf, float dx, float dy, float ds, float dd, float df);
void worldInsertPlatform(float px, float py, float sx, float sy);
void stepWorld(void);
bodyPose* getDiscPlayerPose(void);
bodyPose* getRectPlayerPose(void);
void moveDiscPlayer(float f);
void jumpDiscPlayer(float f);
void transformRectPlayer(float s);
void moveRectPlayer(float f);
#endif
