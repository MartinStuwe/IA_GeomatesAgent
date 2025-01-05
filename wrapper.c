// This is a wrapper for box2d, allowing it to be used as
// dynamic library. Only those functions are currently supported
// that we need for our 'geomates' competition.

#include "wrapper.h"
#include <stdlib.h>

b2WorldDef gWorldDef;
b2WorldId gWorldID;
b2BodyId gDiscPlayer;
b2BodyId gRectPlayer;
bodyElem *gBodies;
float gRectRatio = 4.0f;
float gRectSize;
b2ShapeId gRectShapeID;

bodyPose tmpPose;

// initialize global world structure
void initWorld(float gx, float gy) {
    b2Vec2 gravity;
    gWorldDef = b2DefaultWorldDef();
    gravity.x = gx;
    gravity.y = gy;
    gWorldDef.gravity = gravity;
    gWorldID = b2CreateWorld(&gWorldDef);
    gBodies = NULL;
}

// destroy global world structure
void destroyWorld(void) {
    // free storage for all bodies in list
    bodyElem *nxt = gBodies;
    while (nxt) {
        bodyElem *tmp = nxt->next;
        free(nxt);
        nxt = tmp;
    }
    gBodies = NULL;
    // cleanup by box2d
    b2DestroyWorld(gWorldID);
}

void initPlayers(float rx, float ry, float rs, float rd, float rf, float dx, float dy, float ds, float dd, float df) {
    // initialize the rect player
    gRectRatio = 4.0f;
    gRectSize  = rs;
    
    b2BodyDef rectBodyDef = b2DefaultBodyDef();
    rectBodyDef.type = b2_dynamicBody;
    b2Vec2 position;
    position.x = rx;
    position.y = ry;
    rectBodyDef.position = position;
    
    gRectPlayer = b2CreateBody(gWorldID, &rectBodyDef);
    b2Polygon dBox = b2MakeBox(gRectSize*gRectRatio,gRectSize/gRectRatio);
    b2ShapeDef rectShape = b2DefaultShapeDef();
    rectShape.density = rd;
    rectShape.friction = rf;
    gRectShapeID = b2CreatePolygonShape(gRectPlayer, &rectShape, &dBox);
    
    // initialize the disc player
    b2BodyDef discBodyDef = b2DefaultBodyDef();
    discBodyDef.type = b2_dynamicBody;
    position.x = dx;
    position.y = dy;
    rectBodyDef.position = position;
    
    gDiscPlayer = b2CreateBody(gWorldID, &discBodyDef);
    b2Circle disc;
    disc.radius = ds;
    disc.center.x = 0;
    disc.center.y = 0;
    b2ShapeDef discShapeDef = b2DefaultShapeDef();
    discShapeDef.density = dd;
    discShapeDef.friction = df;
    b2CreateCircleShape(gDiscPlayer, &discShapeDef, &disc);
}

void worldInsertDynamicBox(unsigned int idx, float posx, float posy, float sx, float sy, float density, float friction) {
    b2BodyDef bodyDef = b2DefaultBodyDef();
    bodyDef.type = b2_dynamicBody;
    b2Vec2 position;
    position.x = posx;
    position.y = posy;
    bodyDef.position = position;
    
    bodyElem *newBody = malloc(sizeof(bodyElem));
    if (!newBody) exit(-1); // FIXME: better error handling
    
    newBody->b2Body = b2CreateBody(gWorldID, &bodyDef);
    newBody->next = gBodies; // insert body into global list
    gBodies = newBody;
    b2Polygon dBox = b2MakeBox(sx,sy);
    b2ShapeDef shapeDef = b2DefaultShapeDef();
    shapeDef.density = density;
    shapeDef.friction = friction;
    b2CreatePolygonShape(newBody->b2Body, &shapeDef, &dBox);
}

void worldInsertPlatform(float px, float py, float sx, float sy) {
    b2BodyDef bodyDef = b2DefaultBodyDef();
    bodyDef.type = b2_staticBody;
    b2Vec2 position;
    position.x = 0.5*(px+sx);
    position.y = 0.5*(py+sy);
    bodyDef.position = position;

    b2BodyId platformId = b2CreateBody(gWorldID, &bodyDef);

    b2Polygon dBox = b2MakeBox(fabsf(sx-px),fabsf(sy-py));
    b2ShapeDef shapeDef = b2DefaultShapeDef();
    shapeDef.density = 1.0f;
    shapeDef.friction = 0.3f;
    b2CreatePolygonShape(platformId, &shapeDef, &dBox);
}

int diamondHit(float dx, float dy) {
  
    return 0;
    
}

//
// all about game control and simulation
//

void stepWorld(void) {
    b2World_Step(gWorldID, 1.0f / 60.0f, 4);
}

// search through list of bodies and return pose of requested body
// FIXME: linear search is bad
bodyPose* getPose(unsigned int idx) {
    bodyElem *elem = gBodies;
    while (elem) {
        if (elem->ref == idx) {
            tmpPose.position = b2Body_GetPosition(elem->b2Body);
            tmpPose.rotation = b2Rot_GetAngle(b2Body_GetRotation(elem->b2Body));
        } else elem = elem->next;
    }
    return &tmpPose; // FIXME: signal error if not found
}

bodyPose* getRectPlayerPose(void) {
    tmpPose.position = b2Body_GetPosition(gRectPlayer);
    tmpPose.rotation = b2Rot_GetAngle(b2Body_GetRotation(gRectPlayer));
    tmpPose.size = gRectRatio;
    return &tmpPose;
}

bodyPose* getDiscPlayerPose(void) {
    tmpPose.position = b2Body_GetPosition(gDiscPlayer);
    tmpPose.rotation = b2Rot_GetAngle(b2Body_GetRotation(gDiscPlayer));
    return &tmpPose;
}

void moveRectPlayer(float f) {
    b2Vec2 force;
    force.x = f;
    force.y = 0.0f;
    b2Body_ApplyLinearImpulseToCenter(gRectPlayer, force, 1);
}

void transformRectPlayer(float s) {
    // change aspect ratio
    gRectRatio += s;
    if (gRectRatio < -10.0) gRectRatio = -10;
    if (gRectRatio >  10.0) gRectRatio = 10;
    
    b2Polygon box = b2MakeBox(gRectSize*gRectRatio,gRectSize/gRectRatio);
    b2Shape_SetPolygon (gRectShapeID, &box);
}

void moveDiscPlayer(float f) {
    b2Vec2 force;
    force.x = f;
    force.y = 0.0f;
    b2Body_ApplyLinearImpulseToCenter(gDiscPlayer, force, 1);
}

void jumpDiscPlayer(float f) {
    // FIXME: only jump if disc is currently in contact to an object below!!
    b2Vec2 force;
    force.x = 0.0f;
    force.y = f;
    b2Body_ApplyLinearImpulseToCenter(gDiscPlayer, force, 1);
}
