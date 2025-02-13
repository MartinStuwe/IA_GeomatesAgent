#include <box2d/box2d.h>

#ifndef __WRAPPER_H__
#define __WRAPPER_H__
typedef struct bodyElem {
    b2BodyId b2Body;
    int ref;
    void *next;
} bodyElem;

// for querying pose of player object
typedef struct bodyPose {
    b2Vec2 position;
    float rotation; // for rect only
    float width; // rect only
    float height; // rect only
} bodyPose;

typedef struct growObstacles {
    b2Vec2 pos; // position of rect that is about to grow
    int left, right, bottom, top; // count for objects in directions
} growObstacles;

void initWorld(float gx, float gy);
void destroyWorld(void);
void initPlayers(float rx, float ry, float rs, float ratio, float rd, float rf, float dx, float dy, float ds, float dd, float df);
void worldInsertPlatform(float px, float py, float sx, float sy);
void stepWorld(void);
bodyPose* getDiscPlayerPose(void);
bodyPose* getRectPlayerPose(void);
void moveDiscPlayer(float f);
void jumpDiscPlayer(float f);
void transformRectPlayer(float s); // grow/shrink
void moveRectPlayer(float f); // move left/right
int bodyOnGround(b2BodyId body); // checks if body rests on some object
int pointInRectPlayer(float x, float y);
#endif
