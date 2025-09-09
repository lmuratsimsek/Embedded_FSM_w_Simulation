# 🔁 Embedded FSM Visualization

This project demonstrates a **modular state machine (FSM)** architecture tailored for **embedded systems**, along with a **real-time graphical simulation** using Python and Tkinter.

It is designed to visualize and explain how state transitions occur in a structured embedded system, making it ideal for developers, educators, and system designers who want to both implement and present FSM-based architectures clearly.

![StateMachineVisualization2025-09-0913-50-36-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/1e66ff8e-e45f-4789-adbf-c8d01fc81eca)

## 🎯 Project Goals

- Implement a **reliable and scalable FSM** in Embedded C using **function pointers**
- Include **entry, exit, and main handler** separation per state
- Provide a **visual simulation** of FSM flow via Python GUI
- Emulate real-time system behavior for better understanding and testing

---

## 📂 Project Structure

```
embedded-fsm-visualization/
├── embedded/
│   ├── main.c
│   ├── main.h
│   └── (supporting headers)
│
├── simulation/
│   ├── fsm_visual.py
│   ├── fsm_diagram.png
│   └── video_demo.mp4
│
├── README.md
└── LICENSE
```

---

## ⚙️ FSM Core in C (`main.c` / `main.h`)

### ✳️ `main.h` Overview

Contains:

- Event and state definitions
- Function pointer typedefs
- FSM struct definitions:
  - `stateMachine_t`: state transitions
  - `sComplexFunc_t`: entry/exit/main mapping
  - `mainStruct_Type`: current state tracker

```c
typedef void (*vFuncPtr)(void);

typedef enum eventSM {
    _EVENT_NOT_DETECTED,
    _EVENT_A_DONE, _EVENT_A_FAULT,
    _EVENT_B_ACTIVE, _EVENT_B_PASSIVE,
    _EVENT_TASK2_DONE,
    _EVENT_EXIT_FROM_TASK
} eventSM_t;

typedef struct sComplexFunc {
    vFuncPtr prvMain;
    vFuncPtr prvEntry;
    vFuncPtr prvExit;
} sComplexFunc_t;

typedef struct stateMachine_s {
    vFuncPtr prvSourceFunc;
    vFuncPtr prvTargetFunc;
    eventSM_t eventSM;
} stateMachine_t;

typedef struct mainLoop_s {
    vFuncPtr prvActiveFunc;
    vFuncPtr prvTargetFunc;
    eventSM_t eventSM;
    size_t sizeMainStateMachine;
    sComplexFunc_t complexStateInfo;
    size_t sizeComplexStateMachine;
} mainStruct_Type;
```

---

### ⚙️ `main.c` Logic

The FSM system is initialized and executed in a main loop. Transitions are handled by mapping the current function + event combination to the target state.

#### 🔹 FSM Initialization

```c
static void vMainLoopInit(void) {
    mainStruct.sizeMainStateMachine = sizeof(mainStateMachine) / sizeof(mainStateMachine[0]);
    mainStruct.prvActiveFunc = prvStates_AEventCheck;
    mainStruct.eventSM = _EVENT_NOT_DETECTED;
    mainStruct.sizeComplexStateMachine = sizeof(complexFunc) / sizeof(complexFunc[0]);
}
```

#### 🔹 FSM Main Loop

```c
static void vMainLoop(void) {
    do {
        prvSourceFuncAndEventMapper();
        if (mainStruct.prvActiveFunc != NULL) {
            mainStruct.prvActiveFunc();
        }
    } while (mainStruct.prvActiveFunc != prvExitFromTask);
}
```

#### 🔹 State Transition Mapping

```c
static void prvSourceFuncAndEventMapper(void) {
    for (size_t i = 0; i < mainStruct.sizeMainStateMachine; i++) {
        if (mainStateMachine[i].prvSourceFunc == mainStruct.prvActiveFunc &&
            mainStateMachine[i].eventSM == mainStruct.eventSM) {

            mainStruct.prvTargetFunc = mainStateMachine[i].prvTargetFunc;
            prvEntryAndExitFuncMapper();
            mainStruct.prvActiveFunc = prvFuncTransition;
            mainStruct.eventSM = _EVENT_NOT_DETECTED;
            break;
        }
    }
}
```

#### 🔹 Entry/Exit Function Handler

```c
static void prvFuncTransition(void) {
    if (mainStruct.complexStateInfo.prvExit != NULL)
        mainStruct.complexStateInfo.prvExit();
    if (mainStruct.complexStateInfo.prvEntry != NULL)
        mainStruct.complexStateInfo.prvEntry();
    if (mainStruct.prvTargetFunc != NULL)
        mainStruct.prvActiveFunc = mainStruct.prvTargetFunc;
}
```

#### 🔹 Sample State Functions

```c
static void prvStates_AEventCheck(void) {
    static uint8_t ucAData = 0;
    printf("\nActive Function: prvStates_AEventCheck()");
    mainStruct.eventSM = (ucAData == 0) ? _EVENT_A_DONE : _EVENT_A_FAULT;
}

static void prvEntryState_AEventCheck(void) {
    printf("\nEntry - prvEntryState_AEventCheck");
}

static void prvExitState_AEventCheck(void) {
    printf("\nExit - prvExitState_AEventCheck");
}
```

---

## 🖥️ Python Simulation

Inside the `simulation/` folder:

- `fsm_visual.py` is a real-time state machine simulator using `Tkinter`
- Shows FSM state flow live with colored highlights
- Automatically triggers random events between states
- Entry/Exit functions shown diagonally connected
- All state transitions visualized with directional arrows

```bash
cd simulation/
python fsm_visual.py
```

📷 Example Visual:
<img width="665" height="625" alt="MainStateMachine" src="https://github.com/user-attachments/assets/8971a156-dff9-41bc-8ba1-7161211ad35b" />

---

## ✅ Benefits of This FSM Architecture

- ✅ **Modular and Readable**: Clear separation of logic per state
- 🔁 **Reusable**: Easy to plug new states/events
- 🧩 **Entry/Exit Hooks**: Better control per transition
- 🧪 **Testable**: Logic can be simulated on PC before embedded deployment
- 👀 **Visual Debugging**: Tkinter GUI aids in design & verification

---

## 🚀 Getting Started

### 🧰 Requirements (Python)

- Python 3.7+
- Tkinter (standard lib)

```bash
pip install tk
```

### ⚙️ Build Embedded (STM32 or Bare Metal)

1. Include `main.c`, `main.h` in your project
2. Call `vMainLoopInit()` once
3. Run `vMainLoop()` in your main task or super-loop

---

## 📚 License

Feel free to use and modify. Attribution appreciated.

---

## 🙌 Contributing

Pull requests, ideas, or feature requests are welcome!

---

## 👋 Author

Made by **Murat Şimşek**  
🛠️ Embedded Systems & Software Architecture  
📫 [LinkedIn](https://linkedin.com/in/lmuratsimsek)

