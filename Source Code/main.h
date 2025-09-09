#ifndef INC_MAINLOOP_H_
#define INC_MAINLOOP_H_
/**********************************************************************************************************************************************************
* Include Libraries
**********************************************************************************************************************************************************/
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "main.h"
/**********************************************************************************************************************************************************
* Static Value Declarations
**********************************************************************************************************************************************************/
#define ZERO                                        0
#define ACTIVE                                      1u
#define PASSIVE                                     ZERO
#define sciDEBUG_STATE_MACHINE_FUNCTION_INFO		ACTIVE
#define sciDEBUG_ENTRY_EXIT_SM_INFO                 ACTIVE
/**********************************************************************************************************************************************************
* Function Pointer
**********************************************************************************************************************************************************/
typedef void (*vFuncPtr)(void);
/**********************************************************************************************************************************************************
* Struct and Enum Definitons
**********************************************************************************************************************************************************/
typedef enum eventSM
{
	_EVENT_NOT_DETECTED,
	_EVENT_A_DONE,          _EVENT_A_FAULT,
	_EVENT_B_ACTIVE,        _EVENT_B_PASSIVE,
	_EVENT_TASK2_DONE,
	/** prvExitFromTask() */ _EVENT_EXIT_FROM_TASK

}eventSM_t;

typedef struct sComplexFunc
{
    vFuncPtr                prvMain;
    vFuncPtr                prvEntry;
    vFuncPtr                prvExit;
}sComplexFunc_t;

typedef struct stateMachine_s
{
	vFuncPtr	        prvSourceFunc;
	vFuncPtr 	        prvTargetFunc;
	eventSM_t 	        eventSM;
} stateMachine_t;

typedef struct mainLoop_s
{
    vFuncPtr       prvActiveFunc;
    vFuncPtr       prvTargetFunc;
    eventSM_t 	   eventSM;
    size_t 		   sizeMainStateMachine;
    sComplexFunc_t complexStateInfo;
    size_t         sizeComplexStateMachine;
}mainStruct_Type;

/**********************************************************************************************************************************************************
* Functions Prototype Definations
**********************************************************************************************************************************************************/
static void vMainLoopInit(void);
static void vMainLoop(void);
static void prvSourceFuncAndEventMapper(void);
static void prvFuncTransition(void);
static void prvEntryAndExitFuncMapper(void);
static void prvExitFromTask(void);
static void prvEntryState_AEventCheck(void);
static void prvStates_AEventCheck(void);
static void prvExitState_AEventCheck(void);
static void prvEntryState_BEventCheck(void);
static void prvStates_BEventCheck(void);
static void prvExitState_BEventCheck(void);
static void prvStates_Task2(void);

#endif /* INC_MAINLOOP_H_ */
