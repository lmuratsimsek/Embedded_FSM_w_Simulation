#include "main.h"
/*---------------------------------------------------------------------------------------------------------------------------*/
mainStruct_Type mainStruct;
/*****************************************************************************************************************************
* Entry/Exit State Machine
******************************************************************************************************************************/
static const sComplexFunc_t complexFunc[] =
{
    /**Main Function List                           Entry Function List                         Exit Function List           */
    { prvStates_AEventCheck,     				    prvEntryState_AEventCheck,                  prvExitState_AEventCheck     },
    { prvStates_BEventCheck,     				    prvEntryState_BEventCheck,                  prvExitState_BEventCheck     }
    /* { prvXStates_ExampleFunction,           		prvMainSm_ExampleFuncEntry,                 prvMainSm_ExampleFuncExit	 } */
};
/******************************************************************************************************************************
* Main State Machine
******************************************************************************************************************************/
static const stateMachine_t mainStateMachine[] =
{		/**Source Function List                    Target Function List                 Event For State Machime List         */
		{ prvStates_AEventCheck, 				   prvStates_BEventCheck,				_EVENT_A_DONE           			 },
		{ prvStates_AEventCheck, 				   prvExitFromTask,				        _EVENT_A_FAULT          			 },
		{ prvStates_BEventCheck, 				   prvStates_Task2,					    _EVENT_B_PASSIVE        			 },
		{ prvStates_Task2, 				           prvStates_AEventCheck,			    _EVENT_TASK2_DONE 			         },
		{ prvStates_BEventCheck, 				   prvExitFromTask,				        _EVENT_B_ACTIVE         			 },
		{ prvExitFromTask, 				           prvStates_AEventCheck,				_EVENT_EXIT_FROM_TASK         	     }
};
/*---------------------------------------------------------------------------------------------------------------------------*/
static void vMainLoopInit(void)
{
	mainStruct.sizeMainStateMachine = sizeof(mainStateMachine) / sizeof(mainStateMachine[ZERO]);
	mainStruct.prvActiveFunc = prvStates_AEventCheck;
	mainStruct.eventSM = _EVENT_NOT_DETECTED;
	mainStruct.sizeComplexStateMachine = sizeof(complexFunc) / sizeof(complexFunc[ZERO]);
}
/*---------------------------------------------------------------------------------------------------------------------------*/
static void vMainLoop(void)
{
	do
	{
		prvSourceFuncAndEventMapper();
		if (mainStruct.prvActiveFunc != NULL)
		{
			mainStruct.prvActiveFunc();
		}
	}
	while (mainStruct.prvActiveFunc != prvExitFromTask);
}
/*---------------------------------------------------------------------------------------------------------------------------*/
int main()
{
    vMainLoopInit();
    
    while(1)
    {
        vMainLoop();
    }
    return 0;
}

/*---------------------------------------------------------------------------------------------------------------------------*/
static void prvSourceFuncAndEventMapper(void)
{
	for (size_t sizeMainSM = ZERO; sizeMainSM < mainStruct.sizeMainStateMachine; sizeMainSM++ )
	{
		if (mainStateMachine[sizeMainSM].prvSourceFunc == mainStruct.prvActiveFunc)
		{
			if (mainStateMachine[sizeMainSM].eventSM == mainStruct.eventSM)
			{
				mainStruct.prvTargetFunc = mainStateMachine[sizeMainSM].prvTargetFunc;
                prvEntryAndExitFuncMapper();
				mainStruct.prvActiveFunc = prvFuncTransition;
				mainStruct.eventSM = _EVENT_NOT_DETECTED;
				break;
			}
		}
	}
}
/*---------------------------------------------------------------------------------------------------------------------------*/
static void prvFuncTransition(void)
{
    if(mainStruct.complexStateInfo.prvExit != NULL)
    {
        mainStruct.complexStateInfo.prvExit();
    }
    if(mainStruct.complexStateInfo.prvEntry != NULL)
    {
        mainStruct.complexStateInfo.prvEntry();
    }
    if(mainStruct.prvTargetFunc != NULL)
    {
        mainStruct.prvActiveFunc = mainStruct.prvTargetFunc;
        mainStruct.prvTargetFunc();
    }
}
/*---------------------------------------------------------------------------------------------------------------------------*/
static void prvEntryAndExitFuncMapper(void)
{
    for (size_t sizeComplexFuncIdx = ZERO; sizeComplexFuncIdx < mainStruct.sizeComplexStateMachine; sizeComplexFuncIdx++)
    {
        if (mainStruct.prvActiveFunc == complexFunc[sizeComplexFuncIdx].prvMain)
        {
            mainStruct.complexStateInfo.prvExit = complexFunc[sizeComplexFuncIdx].prvExit;
        }
        if (mainStruct.prvTargetFunc == complexFunc[sizeComplexFuncIdx].prvMain)
        {
            mainStruct.complexStateInfo.prvEntry = complexFunc[sizeComplexFuncIdx].prvEntry;
        }
    }
}
/*---------------------------------------------------------------------------------------------------------------------------*/
static void prvEntryState_AEventCheck(void)
{
    #if (sciDEBUG_ENTRY_EXIT_SM_INFO == ACTIVE)
	{
		printf("\nEntry - prvEntryState_AEventCheck");
	}
	#endif
}
static void prvStates_AEventCheck(void)
{
    static uint8_t ucAData = ZERO;
	#if (sciDEBUG_STATE_MACHINE_FUNCTION_INFO == ACTIVE)
	{
		printf("\nActive Function: prvStates_AEventCheck()");
	}
	#endif
	
	if (ucAData == ZERO)
 	{
 	    mainStruct.eventSM = _EVENT_A_DONE;    
 	}
 	else /* ucBData != ZERO */
 	{
 	    mainStruct.eventSM = _EVENT_A_FAULT;    
 	}
}
static void prvExitState_AEventCheck(void)
{
    #if (sciDEBUG_ENTRY_EXIT_SM_INFO == ACTIVE)
	{
		printf("\nExit - prvExitState_AEventCheck");
	}
	#endif
}
/*---------------------------------------------------------------------------------------------------------------------------*/
static void prvEntryState_BEventCheck(void)
{
    #if (sciDEBUG_ENTRY_EXIT_SM_INFO == ACTIVE)
	{
		printf("\nExit - prvEntryState_BEventCheck");
	}
	#endif
}
static void prvStates_BEventCheck(void)
{
    static uint8_t ucBData = ZERO;
 	#if (sciDEBUG_STATE_MACHINE_FUNCTION_INFO == ACTIVE)
 	{
 		printf("\nActive Function: prvStates_BEventCheck()");
 	}
 	#endif
 	
 	if (ucBData == ZERO)
 	{
 	    mainStruct.eventSM = _EVENT_B_PASSIVE;    
 	}
 	else /* ucBData != ZERO */
 	{
 	    mainStruct.eventSM = _EVENT_B_ACTIVE;    
 	}
}
static void prvExitState_BEventCheck(void)
{
    #if (sciDEBUG_ENTRY_EXIT_SM_INFO == ACTIVE)
	{
		printf("\nExit - prvExitState_BEventCheck");
	}
	#endif
}
/*---------------------------------------------------------------------------------------------------------------------------*/
static void prvStates_Task2(void)
{
    #if (sciDEBUG_STATE_MACHINE_FUNCTION_INFO == ACTIVE)
 	{
 		printf("\nActive Function: prvStates_Task2()");
 	}
 	#endif
 	mainStruct.eventSM = _EVENT_TASK2_DONE;
}
/*---------------------------------------------------------------------------------------------------------------------------*/
static void prvExitFromTask(void)
{
	#if (sciDEBUG_STATE_MACHINE_FUNCTION_INFO == ACTIVE)
	{
		printf("\nActive Function: prvExitFromTask()");
	}
	#endif
	mainStruct.eventSM = _EVENT_EXIT_FROM_TASK;
}
